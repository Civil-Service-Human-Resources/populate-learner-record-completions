import pickle
import LearningPeriodUtil
import LearnerRecordDAO
import json
from datetime import datetime
import logging
import CsrsService
import os
import math

logging.basicConfig(filename='debug.log', level=logging.DEBUG)

module_records = pickle.load(open("data/last_mandatory_module_completions.pkl", "rb"))

logging.debug(f"Loaded {len(module_records)} last module completions.")

courses = pickle.load(open("data/courses.pkl", "rb"))
logging.debug(f"Loaded {len(courses)} courses.")

incomplete_completion_records = []

for (index,record) in enumerate(module_records):
    _ = os.system("clear")
    percentage_completed = str(math.floor((index/len(module_records))*100))
    print(f"Processing {index+1} of {len(module_records)} ({percentage_completed}%)")
    print(f"Incomplete records found: {len(incomplete_completion_records)}")
    print()
    os.system("tail -n20 debug.log")

    user_id = record[0]
    organisation_code = record[1]
    course_id = record[2]
    last_module_completion_date = record[3]
    created_at = record[4]

    logging.debug(f"Processing user_id: {user_id}, organisation_code: {organisation_code}, course_id: {course_id}, last completion date: {last_module_completion_date}")

    organisation_hierarchy = CsrsService.get_organisation_hierarchy(organisation_code)
    logging.debug(f" - Organisation hierarchy for code {organisation_code}: {organisation_hierarchy}")
    
    course = next((course for course in courses if course["id"] == course_id), None)
    logging.debug(f" - Course for course_id {course_id}: {course["title"] if course else 'Not Found'}")

    if course is None:
        continue

    for organisation in organisation_hierarchy:
        audience = next((a for a in course["audiences"] if organisation[2] in a["departments"]), None)
    
        if audience is not None:
            break

    logging.debug(f" - Audience for organisation {organisation_code}: {audience if audience else 'Not Found'}")

    if audience is None or "frequency" not in audience:
        learning_period = datetime.fromtimestamp(0)
    elif "frequency" in audience and audience["frequency"] is not None:
        required_by = audience["requiredBy"]
        frequency = audience["frequency"]
        logging.debug(f" - Required by: {required_by}, Frequency: {frequency}")
        learning_period = LearningPeriodUtil.get_current_learning_period(required_by, frequency)
    
    logging.debug(f" - Learning period start date: {learning_period}")

    mandatory_module_ids = [module["id"] for module in course["modules"] if not module["optional"]]
    mandatory_module_ids.sort()
    mandatory_module_count = len(mandatory_module_ids)
    logging.debug(f" - Mandatory module count for course_id {course_id}: {mandatory_module_count}")
    logging.debug(f" - Mandatory module IDs: {mandatory_module_ids}")

    module_record_for_user_and_course = LearnerRecordDAO.get_required_module_completions_for_user_and_course(user_id, course_id, learning_period)
    module_record_mandatory_module_ids = [m[2] for m in module_record_for_user_and_course]
    module_record_mandatory_module_ids.sort()
    logging.debug(f" - Module records for user_id {user_id} and course_id {course_id}: {len(module_record_for_user_and_course)} found")

    if mandatory_module_count != len(module_record_mandatory_module_ids):
        logging.debug(f" - Not all mandatory modules completed for user_id {user_id} in course_id {course_id}.")
        continue

    if mandatory_module_ids != module_record_mandatory_module_ids:
        logging.debug(f" - Module IDs in course and module record are different: Module IDs in course: {mandatory_module_ids}, Module record: {module_record_mandatory_module_ids}")
        continue

    logging.debug(f" - All mandatory modules completed for user_id {user_id} in course_id {course_id}.")

    logging.debug(f" - Getting completion events for user {user_id}, course {course_id} and learning period starting from {learning_period}...")
    completion_events = LearnerRecordDAO.get_course_completion_events(user_id, course_id, learning_period)
    logging.debug(f" - {len(completion_events)} completion events found.")

    if len(completion_events) > 0:
        logging.debug(f" - Completion event exists for user_id {user_id} in course_id {course_id}. No change required")
        continue

    logging.debug(f" - 🟡 No completion event found for user_id {user_id} in course_id {course_id}. Marking as incomplete.")

    incomplete_completion_records.append({
        "user_id": user_id,
        "course_id": course_id,
        "completion_timestamp": datetime.strftime(last_module_completion_date, "%Y-%m-%dT%H:%M:%S"),
        "created_at": datetime.strftime(created_at, "%Y-%m-%dT%H:%M:%S")
    })
            
logging.debug(f"Total incomplete completion records found: {len(incomplete_completion_records)}")
logging.debug("Saving to plan.json file...")
json.dump(incomplete_completion_records, open("data/plan.json", "w"), indent=4, default=str)
logging.debug("Data saved to plan.json successfully.")