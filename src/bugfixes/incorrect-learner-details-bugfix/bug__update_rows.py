import json
import psycopg
import modules.config.ConfigService as ConfigService

postgres_config = ConfigService.get_config()["postgres"]

connection = psycopg.connect(
    dbname="reporting",
    user=postgres_config["username"],
    password=postgres_config["password"],
    host=postgres_config["host"]
)

entries = json.load(open('data/wrong_entries.json'))["wrong_entries"]

for entry in entries:
    event_id = entry['incorrect_entry']['event_id']
    print(f"Incorrect entry event_id: {event_id}")

    email = entry['correct_learner_details']['user_email']
    organisation_id = entry['correct_learner_details']['organisation_id']
    organisation_name = entry['correct_learner_details']['organisation_name']
    profession_id = entry['correct_learner_details']['profession_id']
    profession_name = entry['correct_learner_details']['profession_name']
    grade_id = entry['correct_learner_details']['grade_id']
    grade_name = entry['correct_learner_details']['grade_name']

    print(f" - Updating to email: {email}, organisation_id: {organisation_id}, organisation_name: {organisation_name}, profession_id: {profession_id}, profession_name: {profession_name}, grade_id: {grade_id}, grade_name: {grade_name}")

    update_query = """UPDATE course_completion_events
        SET user_email = %s,
            organisation_id = %s,
            organisation_name = %s,
            profession_id = %s,
            profession_name = %s,
            grade_id = %s,
            grade_name = %s
        WHERE event_id = %s;"""
    
    cursor = connection.cursor()
    cursor.execute(update_query, (
        email,
        organisation_id,
        organisation_name,
        profession_id,
        profession_name,
        grade_id,
        grade_name,
        event_id
    ))
    connection.commit()
    cursor.close()