import modules.utils.LearningPeriodUtil as LearningPeriodUtil
import json
from datetime import datetime
import logging
import os
import modules.learner.LearnerService as LearnerService
import modules.audience.AudienceService as AudienceService
import modules.learningCatalogue.LearningCatalogueAppDataDAO as LearningCatalogueAppDataDAO
import modules.csrs.CsrsAppDataDAO as CsrsAppDataDAO
import modules.utils.ArrayUtil as ArrayUtil
import modules.learnerRecord.LearnerRecordAppDataDAO as LearnerRecordAppDataDAO
import modules.reporting.ReportingAppDataDAO as ReportingAppDataDAO
import modules.learnerRecord.LearnerRecordService as LearnerRecordService
import traceback
import pandas as pd

logging.basicConfig(filename='/logs/debug4.log', level=logging.DEBUG)

def run():
    script_start_time = datetime.now()

    module_records = LearnerRecordAppDataDAO.get_last_mandatory_module_completions()
    logging.debug(f"Loaded {len(module_records)} last module completions.")
    courses = LearningCatalogueAppDataDAO.get_all_courses()
    logging.debug(f"Loaded {len(courses)} courses.")

    organisations = CsrsAppDataDAO.get_all_organisations()
    logging.debug(f"Loaded {len(organisations)} organisations.")

    reporting_data = ReportingAppDataDAO.get_reporting_data()
    reporting_data_df = pd.DataFrame(reporting_data, columns=[
        "user_id",
        "user_email",
        "organisation_id",
        "organisation_name",
        "profession_id",
        "profession_name",
        "grade_id",
        "grade_name",
        "event_timestamp"
    ])
    reporting_data_df = reporting_data_df.set_index(['user_id']).sort_index()
    logging.debug(f"Loaded {len(reporting_data)} reporting data records.")

    module_completions = LearnerRecordAppDataDAO.get_module_completions()
    module_completions_df = pd.DataFrame(module_completions, columns=['user_id', 'course_id', 'module_id', 'completion_date'])
    module_completions_df = module_completions_df.set_index(['user_id', 'course_id']).sort_index()
    module_completions_df['completion_date'] = pd.to_datetime(module_completions_df['completion_date'])
    logging.debug(f"Loaded {len(module_completions)} module completions.")

    course_completion_events = LearnerRecordAppDataDAO.get_course_completion_events()
    course_completion_events_df = pd.DataFrame(course_completion_events, columns=["learner_id", "resource_id", "event_timestamp"])
    course_completion_events_df['event_timestamp'] = pd.to_datetime(course_completion_events_df['event_timestamp'])
    course_completion_events_df = course_completion_events_df.set_index(['learner_id', 'resource_id']).sort_index()
    logging.debug(f"Loaded {len(course_completion_events)} course completion events.")

    csrs_learner_details = CsrsAppDataDAO.get_all_learner_details()
    csrs_learner_details_df = pd.DataFrame(csrs_learner_details, columns=["user_id", "user_email", "organisation_id", "organisation_name", "profession_id", "profession_name", "grade_id", "grade_name"])
    csrs_learner_details_df = csrs_learner_details_df.set_index(['user_id']).sort_index()
    logging.debug(f"Loaded {len(csrs_learner_details)} learner details from CSRS.")

    incomplete_completion_records = []

    record_count = len(module_records)
    for (index,record) in enumerate(module_records):
        try:
            logging.debug(f"Starting record number {index}: {record}...")
            _ = os.system("clear")
            print(f"{index + 1} / {record_count}")
            print(f"Incomplete records found: {len(incomplete_completion_records)}")

            user_id = record[0]
            last_module_completion_date = record[3]
            learner_details = LearnerService.get_learner_details(reporting_data_df, csrs_learner_details_df, user_id, last_module_completion_date.strftime("%Y-%m-%dT%H:%M:%S"))
            logging.debug(f"- Found learner details: {learner_details}")

            course_id = record[2]
            created_at = record[4]

            logging.debug(f"- Processing user_id: {user_id}, course_id: {course_id}, last completion date: {last_module_completion_date}")
            
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

            module_record_for_user_and_course = LearnerRecordService.get_mandatory_module_completions_for_user_and_course(module_completions_df, user_id, course_id, learning_period_info['start_date'].strftime("%Y-%m-%d %H:%M"), learning_period_info['end_date'].strftime("%Y-%m-%d %H:%M"))
            module_record_mandatory_module_ids = module_record_for_user_and_course["module_id"].tolist()
            logging.debug(f" - User {user_id} completed {len(module_record_mandatory_module_ids)} modules for course with ID {course_id}")

            if mandatory_module_count != len(module_record_mandatory_module_ids):
                logging.debug(f" - Not all mandatory modules completed for user_id {user_id} in course_id {course_id}.")
                continue

            if not ArrayUtil.compare_string_arrays(mandatory_module_ids, module_record_mandatory_module_ids):
                logging.debug(f" - Module IDs in course and module record are different: Module IDs in course: {mandatory_module_ids}, Module record: {module_record_mandatory_module_ids}")
                continue

            logging.debug(f" - All mandatory modules completed for user_id {user_id} in course_id {course_id}.")

            logging.debug(f" - Getting completion events for user {user_id}, course {course_id} and learning period {learning_period_info['start_date']} to {learning_period_info['end_date']}...")
            completion_events = LearnerRecordService.get_course_completion_events_for_user_and_course(course_completion_events_df, user_id, course_id, learning_period_info['start_date'], learning_period_info['end_date'])

            if completion_events is not None and len(completion_events) > 0:
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
            logging.debug(f"- Incomplete completion record added to list: {record}. Total incomplete records so far: {len(incomplete_completion_records)}")
        except Exception as e:
            logging.error(f"- Processing completion failed: {e}")
            logging.error(traceback.format_exc())
                
    logging.debug(f"Total incomplete completion records found: {len(incomplete_completion_records)}")
    logging.debug("Saving to plan.json file...")
    json.dump(incomplete_completion_records, open("/app-data/plan.json", "w"), indent=4, default=str)
    logging.debug("Data saved to plan.json successfully.")
    
    script_end_time = datetime.now()

    print(f"Script took {(script_end_time - script_start_time).seconds} seconds to run")

run()