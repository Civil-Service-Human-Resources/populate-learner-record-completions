import json
import modules.learnerRecord.LearnerRecordDAO as LearnerRecordDAO
import json
import pickle
import modules.reporting.ReportingDAO as ReportingDAO
import uuid
import logging

logging.basicConfig(filename='/logs/debug.log', level=logging.DEBUG)

plan_data = json.load(open("/app-data/plan.json", "r"))
logging.debug(f"Loaded {len(plan_data)} plan items.")
courses = pickle.load(open("/app-data/courses.pkl", "rb"))
logging.debug(f"Loaded {len(courses)} courses.")

learner_record_event_rows = [{
    "learner_id": p["user_id"],
    "resource_id": p["course_id"],
    "event_timestamp": p["completion_timestamp"]
} for p in plan_data]

logging.debug(f"Prepared {len(learner_record_event_rows)} learner record event rows.")

def run():
	apply_results = LearnerRecordDAO.insert_learner_record_events(learner_record_event_rows)
	logging.info(f"Inserted learner record events with results: {apply_results}")

	course_completion_events_rows = []

	logging.debug("Preparing course completion events...")
	for item in plan_data:
		logging.debug(f"Processing plan item for user_id: {item['user_id']}, course_id: {item['course_id']}")
		
		if "learner_details" in item:
			course_completion_events_rows.append({
				"external_id": str(uuid.uuid4()),
				"user_id": item["user_id"],
				"user_email": item["learner_details"]["user_email"],
				"course_id": item["course_id"],
				"course_title": next((c["title"] for c in courses if c["id"] == item["course_id"]), None),
				"event_timestamp": item["completion_timestamp"],
				"organisation_id": item["learner_details"]["organisation_id"],
				"profession_id": item["learner_details"]["profession_id"],
				"grade_id": item["learner_details"]["grade_id"],
				"grade_name": item["learner_details"]["grade_name"],
				"profession_name": item["learner_details"]["profession_name"],
				"organisation_name": item["learner_details"]["organisation_name"]
			})
			logging.debug(f"  - Added course completion event for user_id: {item['user_id']}, course_id: {item['course_id']}")
		else:
			logging.warning(f"- Learner details not found for user_id: {item['user_id']}")

	ReportingDAO.insert_course_completion_events(course_completion_events_rows)
	logging.info(f"Inserted {len(course_completion_events_rows)} course completion events.")

	apply_output = {
		"learner_record_events": apply_results,
		"reporting_course_completion_events": course_completion_events_rows
	}

	json.dump(apply_output, open("/app-data/apply.json", "w"), indent=4)
	logging.debug("Saved apply output to /app-data/apply.json")

run()