import psycopg
import config
import uuid
import DateUtil

pg_config = config.get_config()["postgres"]

print(pg_config)

connection = psycopg.connect(
    dbname="reporting",
    user=pg_config["username"],
    password=pg_config["password"],
    host=pg_config["host"]
)

def get_learners_details(learner_ids):
    sql_query = """select 
        cce.user_id, 
        max(cce.user_email) as user_email,  
        max(cce.organisation_id) as organisation_id,
        max(cce.organisation_name) as organisation_name,
        max(cce.profession_id) as profession_id,
        max(cce.profession_name) as profession_name,
        max(cce.grade_id) as grade_id,
        max(cce.grade_name) as grade_name
        from course_completion_events cce 
        where cce.user_id = any(%s)
        group by cce.user_id;""";
    
    cursor = connection.cursor()
    cursor.execute(sql_query, (learner_ids,))
    result = cursor.fetchall()
    cursor.close()
    return result
    
def insert_course_completion_events(events):
    cursor = connection.cursor()
    for event in events:
        completion_date = event["event_timestamp"]
        create_partition_query = f"""CREATE TABLE IF NOT EXISTS course_completion_events_{DateUtil.get_date_partition_name(completion_date)} PARTITION OF course_completion_events
            FOR VALUES FROM ('{DateUtil.get_partition_dates(completion_date)["start_date"]}') TO ('{DateUtil.get_partition_dates(completion_date)["end_date"]}');"""
        cursor.execute(create_partition_query)
    
    insert_query = f"""INSERT INTO course_completion_events 
        (external_id, user_id, user_email, course_id, course_title, event_timestamp, organisation_id, profession_id, grade_id, grade_name, profession_name, organisation_name) 
        VALUES 
        (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
    
    rows = [(event["external_id"], event["user_id"], event["user_email"], event["course_id"], event["course_title"], event["event_timestamp"], event["organisation_id"], event["profession_id"], event["grade_id"], event["grade_name"], event["profession_name"], event["organisation_name"],) for event in events]
    
    cursor.executemany(insert_query, rows)
    connection.commit()
    cursor.close()