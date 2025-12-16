import json
import LearnerRecordDAO
import json
import pickle
import ReportingDAO
import uuid

plan_data = json.load(open("data/plan.json", "r"))
learner_details = pickle.load(open("data/learner_details.pkl", "rb"))
courses = pickle.load(open("data/courses.pkl", "rb"))

event_rows = [{
    "learner_id": p["user_id"],
    "resource_id": p["course_id"],
    "event_timestamp": p["completion_timestamp"]
} for p in plan_data]

apply_results = LearnerRecordDAO.insert_learner_record_events_in_batches(event_rows)
json.dump(apply_results, open("data/apply.json", "w"), indent=4)

course_completion_events_rows = []

for item in plan_data:
	learner = next((ld for ld in learner_details if ld[0] == item['user_id']), None)
	
	if learner is not None:
		course_completion_events_rows.append({
			"external_id": str(uuid.uuid4()),
			"user_id": item["user_id"],
			"user_email": learner[1],
			"course_id": item["course_id"],
			"course_title": next((c["title"] for c in courses if c["id"] == item["course_id"]), None),
			"event_timestamp": item["completion_timestamp"],
			"organisation_id": learner[2],
			"profession_id": learner[4],
			"grade_id": learner[6],
			"grade_name": learner[7],
			"profession_name": learner[5],
			"organisation_name": learner[3]
		})
	else:
		print(f"Learner details not found for user_id: {item['user_id']}")

ReportingDAO.insert_course_completion_events(course_completion_events_rows)