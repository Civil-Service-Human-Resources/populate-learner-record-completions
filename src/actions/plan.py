import pickle
import modules.utils.LearningPeriodUtil as LearningPeriodUtil
import modules.learnerRecord.LearnerRecordDAO as LearnerRecordDAO
import json
from datetime import datetime
import logging
import os
import math
import modules.learner.LearnerService as LearnerService
import modules.audience.AudienceService as AudienceService
import modules.learningCatalogue.LearningCatalogueAppDataDAO as LearningCatalogueAppDataDAO
import modules.csrs.CsrsAppDataDAO as CsrsAppDataDAO
import modules.utils.ArrayUtil as ArrayUtil

logging.basicConfig(filename='/logs/debug.log', level=logging.DEBUG)

def run():
    module_records = pickle.load(open("/app-data/last_mandatory_module_completions.pkl", "rb"))
    logging.debug(f"Loaded {len(module_records)} last module completions.")

    courses = LearningCatalogueAppDataDAO.get_all_courses()
    logging.debug(f"Loaded {len(courses)} courses.")

    organisations = CsrsAppDataDAO.get_all_organisations()
    logging.debug(f"Loaded {len(organisations)} organisations.")

    incomplete_completion_records = []

    for (index,record) in enumerate(module_records):
        _ = os.system("clear")
        percentage_completed = str(math.floor((index/len(module_records))*100))
        print(f"Processing {index+1} of {len(module_records)} ({percentage_completed}%)")
        print(f"Incomplete records found: {len(incomplete_completion_records)}")

        user_id = record[0]
        last_module_completion_date = record[3]
        learner_details = LearnerService.get_learner_details(user_id, last_module_completion_date.strftime("%Y-%m-%dT%H:%M:%S"))

        organisation_code = next(organisation[2] for organisation in organisations if organisation[0] == learner_details["organisation_id"])
        course_id = record[2]
        
        created_at = record[4]

        logging.debug(f"Processing user_id: {user_id}, organisation_code: {organisation_code}, course_id: {course_id}, last completion date: {last_module_completion_date}")
        
        course = next((course for course in courses if course["id"] == course_id), None)
        logging.debug(f" - Course for course_id {course_id}: {course["title"] if course else 'Not Found'}")

        if course is None:
            logging.debug(f" - Course with id {course_id} not found. Skipping to next record.")
            continue

        audience = AudienceService.get_audience_for_organisation(course["audiences"], learner_details["organisation_id"])
        logging.debug(f" - Audience for user: {audience if audience else 'Not Found'}")

        required_by = None if (audience is None or "requiredBy" not in audience or audience["requiredBy"] is None) else audience["requiredBy"]
        frequency = None if (required_by is None or "frequency" not in audience or audience["frequency"] is None) else audience["frequency"]
        learning_period_info = LearningPeriodUtil.get_learning_period_for_date(last_module_completion_date.strftime("%Y-%m-%dT%H:%M:%S"), required_by, frequency)

        logging.debug(f" - Learning period start date: {learning_period_info['start_date']}, end date: {learning_period_info['end_date']}")

        mandatory_module_ids = [module["id"] for module in course["modules"] if not module["optional"]]
        mandatory_module_count = len(mandatory_module_ids)
        logging.debug(f" - Mandatory module count for course_id {course_id}: {mandatory_module_count}")
        logging.debug(f" - Mandatory module IDs: {mandatory_module_ids}")

        module_record_for_user_and_course = LearnerRecordDAO.get_required_module_completions_for_user_and_course(user_id, course_id, learning_period_info['start_date'].strftime("%Y-%m-%d %H:%M"), learning_period_info['end_date'].strftime("%Y-%m-%d %H:%M"))
        module_record_mandatory_module_ids = [m[2] for m in module_record_for_user_and_course]
        logging.debug(f" - Module records for user_id {user_id} and course_id {course_id}: {len(module_record_for_user_and_course)} found")

        if mandatory_module_count != len(module_record_mandatory_module_ids):
            logging.debug(f" - Not all mandatory modules completed for user_id {user_id} in course_id {course_id}.")
            continue

        if not ArrayUtil.compare_string_arrays(mandatory_module_ids, module_record_mandatory_module_ids):
            logging.debug(f" - Module IDs in course and module record are different: Module IDs in course: {mandatory_module_ids}, Module record: {module_record_mandatory_module_ids}")
            continue

        logging.debug(f" - All mandatory modules completed for user_id {user_id} in course_id {course_id}.")

        logging.debug(f" - Getting completion events for user {user_id}, course {course_id} and learning period {learning_period_info['start_date']} to {learning_period_info['end_date']}...")
        completion_events = LearnerRecordDAO.get_course_completion_events(user_id, course_id, learning_period_info['start_date'], learning_period_info['end_date'])
        logging.debug(f" - {len(completion_events)} completion events found.")

        if len(completion_events) > 0:
            logging.debug(f" - Completion event exists for user_id {user_id} in course_id {course_id}. No change required")
            continue

        logging.debug(f" - 🟡 No completion event found for user_id {user_id} in course_id {course_id}. Marking as incomplete.")

        logging.debug(f" - Fetching historical learner details for user_id: {user_id} as of date: {last_module_completion_date}...")

        record = {
            "user_id": user_id,
            "course_id": course_id,
            "completion_timestamp": datetime.strftime(last_module_completion_date, "%Y-%m-%dT%H:%M:%S"),
            "created_at": datetime.strftime(created_at, "%Y-%m-%dT%H:%M:%S")
        }
        if learner_details is not None:
            logging.debug(f" - Learner details found: {learner_details}")
            record["learner_details"] = learner_details
        else:
            logging.debug(f" - Learner details not found for user_id: {user_id}")
        incomplete_completion_records.append(record)
                
    logging.debug(f"Total incomplete completion records found: {len(incomplete_completion_records)}")
    logging.debug("Saving to plan.json file...")
    json.dump(incomplete_completion_records, open("/app-data/plan.json", "w"), indent=4, default=str)
    logging.debug("Data saved to plan.json successfully.")

run()