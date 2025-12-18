import psycopg
import config
import DateUtil

pg_config = config.get_config()["postgres"]

connection = psycopg.connect(
    dbname="reporting",
    user=pg_config["username"],
    password=pg_config["password"],
    host=pg_config["host"]
)

def get_learner_details_around_date(learner_id, date, interval = '1 month'):
    sql_query = f"""select 
        cce.user_id, 
        cce.user_email as user_email,  
        cce.organisation_id as organisation_id,
        cce.organisation_name as organisation_name,
        cce.profession_id as profession_id,
        cce.profession_name as profession_name,
        cce.grade_id as grade_id,
        cce.grade_name as grade_name,
        cce.event_timestamp
        from course_completion_events cce 
        where cce.user_id = %s
        AND cce.event_timestamp BETWEEN %s - INTERVAL '{interval}'
            AND %s + INTERVAL '{interval}'
        and cce.event_timestamp != %s
        order by cce.event_timestamp desc
        limit 1;""";
    
    cursor = connection.cursor()
    dt = DateUtil.get_as_datetime(date)
    cursor.execute(sql_query, (learner_id, dt, dt, dt,))
    result = cursor.fetchone()
    cursor.close()
    return result

def get_learner_details(learner_id: str, date: str = DateUtil.get_date_now_as_string()):
    intervals = ['1 month', '2 months', '3 months', '1 year', '10 years']
    
    learner = None

    for interval in intervals:
        learner = get_learner_details_around_date(learner_id, date, interval)
        if learner is not None:
            break

    return learner
    
def insert_course_completion_events(events):
    cursor = connection.cursor()
    for event in events:
        completion_date = event["event_timestamp"]
        create_partition_query = f"""CREATE TABLE IF NOT EXISTS {DateUtil.get_date_partition_name(completion_date)} PARTITION OF course_completion_events
            FOR VALUES FROM ('{DateUtil.get_partition_dates(completion_date)["start_date"]}') TO ('{DateUtil.get_partition_dates(completion_date)["end_date"]}');"""
        cursor.execute(create_partition_query)

        create_index_query = f"""CREATE INDEX IF NOT EXISTS {DateUtil.get_date_partition_name(completion_date)}_course_id_idx ON {DateUtil.get_date_partition_name(completion_date)} (course_id);
        CREATE INDEX IF NOT EXISTS {DateUtil.get_date_partition_name(completion_date)}_event_timestamp_idx ON {DateUtil.get_date_partition_name(completion_date)} (event_timestamp);
        CREATE INDEX IF NOT EXISTS {DateUtil.get_date_partition_name(completion_date)}_grade_id_idx ON {DateUtil.get_date_partition_name(completion_date)} (grade_id);
        CREATE INDEX IF NOT EXISTS {DateUtil.get_date_partition_name(completion_date)}_organisation_id_idx ON {DateUtil.get_date_partition_name(completion_date)} (organisation_id);
        CREATE INDEX IF NOT EXISTS {DateUtil.get_date_partition_name(completion_date)}_profession_id_idx ON {DateUtil.get_date_partition_name(completion_date)} (profession_id);"""
    
        cursor.execute(create_index_query)
        
    insert_query = f"""INSERT INTO course_completion_events 
        (external_id, user_id, user_email, course_id, course_title, event_timestamp, organisation_id, profession_id, grade_id, grade_name, profession_name, organisation_name) 
        VALUES 
        (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
    
    rows = [(event["external_id"], event["user_id"], event["user_email"], event["course_id"], event["course_title"], event["event_timestamp"], event["organisation_id"], event["profession_id"], event["grade_id"], event["grade_name"], event["profession_name"], event["organisation_name"],) for event in events]
    
    cursor.executemany(insert_query, rows)
    connection.commit()
    cursor.close()