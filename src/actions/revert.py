import json
import modules.learnerRecord.LearnerRecordDAO as LearnerRecordDAO
import modules.reporting.ReportingDAO as ReportingDAO
import logging

logging.basicConfig(filename='/logs/debug.log', level=logging.DEBUG)

apply_data = json.load(open("/app-data/apply.json", "r"))

learner_record_events = apply_data["learner_record_events"]
reporting_course_completion_events = apply_data["reporting_course_completion_events"]

learner_record_events_ids = [event["row_id"] for event in learner_record_events]
reporting_course_completion_events_external_ids = [event["external_id"] for event in reporting_course_completion_events]

logging.debug(f"Deleting {len(learner_record_events_ids)} learner record events...")
deleted_learner_record_events_count = LearnerRecordDAO.delete_learner_record_events_by_ids(learner_record_events_ids)
logging.info(f"Deleted {deleted_learner_record_events_count} learner record events.")

logging.debug(f"Deleting {len(reporting_course_completion_events_external_ids)} reporting course completion events...")
deleted_reporting_course_completion_events_count = ReportingDAO.delete_course_completion_events_by_external_ids(reporting_course_completion_events_external_ids)
logging.info(f"Deleted {deleted_reporting_course_completion_events_count} reporting course completion events.")

logging.info("Revert process completed.")