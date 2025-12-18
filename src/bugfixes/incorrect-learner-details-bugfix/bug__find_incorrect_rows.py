import json
import ReportingDAO

reporting = json.load(open('data/reporting.json'))

wrong_entries = []

for row in reporting["reporting"]:
	learner = ReportingDAO.get_learner_details_around_date(row["user_id"], row["event_timestamp"])

	if learner is None:
		learner = ReportingDAO.get_learner_details_around_date(row["user_id"], row["event_timestamp"], '2 months')

	if learner is None:
		learner = ReportingDAO.get_learner_details_around_date(row["user_id"], row["event_timestamp"], '3 months')

	if learner is None:
		learner = ReportingDAO.get_learner_details_around_date(row["user_id"], row["event_timestamp"], '1 year')

	if learner is None:
		learner = ReportingDAO.get_learner_details_around_date(row["user_id"], row["event_timestamp"], '10 years')

	if learner is None:
		print(f"Learner details not found for user_id: {row['user_id']} at {row['event_timestamp']}")
		continue

	user_id = row["user_id"]
	user_email = row["user_email"]
	organisation_name = row["organisation_name"]
	organisation_id = row["organisation_id"]
	grade_name = row["grade_name"]
	grade_id = row["grade_id"]
	profession_name = row["profession_name"]
	profession_id = row["profession_id"]

	same_email = learner[1] == user_email
	same_organisation = learner[3] == organisation_name
	same_organisation_id = learner[2] == organisation_id
	same_grade = learner[7] == grade_name
	same_grade_id = learner[6] == grade_id
	same_profession = learner[5] == profession_name
	same_profession_id = learner[4] == profession_id

	if not (same_email and same_organisation and same_organisation_id and same_grade and same_grade_id and same_profession and same_profession_id):
			wrong_entries.append({
				"user_id": user_id,
				"incorrect_entry": row,
				"correct_learner_details": {
					"user_email": learner[1],
					"organisation_id": learner[2],
					"organisation_name": learner[3],
					"profession_id": learner[4],
					"profession_name": learner[5],
					"grade_id": learner[6],
					"grade_name": learner[7]
				}
			})

print("Wrong entries:", len(wrong_entries))
with open('data/wrong_entries.json', 'w') as f:
	json.dump({"wrong_entries": wrong_entries}, f, indent=4)