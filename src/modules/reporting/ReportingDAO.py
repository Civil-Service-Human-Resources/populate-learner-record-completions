import modules.utils.DateUtil as DateUtil
import modules.database.PostgresConnection as PostgresConnection

def get_completions_for_learners(learner_ids, start_date, end_date):
    with PostgresConnection.get_connection() as connection:
        with connection.cursor() as cursor:
            tmp_user_ids_query = """CREATE TEMP TABLE tmp_user_ids (
                    user_id text
                ) ON COMMIT DROP;"""
            
            cursor.execute(tmp_user_ids_query)

            with cursor.copy("COPY tmp_user_ids (user_id) FROM STDIN") as copy:
                for learner_id in learner_ids:
                    copy.write_row((learner_id,))

            query = """SELECT
                    cce.user_id as user_id,
                    cce.user_email as user_email,  
                    cce.organisation_id as organisation_id,
                    cce.organisation_name as organisation_name,
                    cce.profession_id as profession_id,
                    cce.profession_name as profession_name,
                    cce.grade_id as grade_id,
                    cce.grade_name as grade_name,
                    cce.event_timestamp as event_timestamp
                FROM course_completion_events cce
                JOIN tmp_user_ids t USING (user_id)
                WHERE cce.event_timestamp BETWEEN %s - INTERVAL '1 year' AND %s + INTERVAL '1 year';"""
            cursor.execute(query, (DateUtil.get_as_datetime(start_date), DateUtil.get_as_datetime(end_date)))

            for user_id, user_email, organisation_id, organisation_name, profession_id, profession_name, grade_id, grade_name, event_timestamp in cursor:
                yield user_id, user_email, organisation_id, organisation_name, profession_id, profession_name, grade_id, grade_name, event_timestamp

def get_learner_details_around_date(learner_id, date):
    interval = '2 years'

    sql_query = f"""select 
        cce.user_email as user_email,  
        cce.organisation_id as organisation_id,
        cce.organisation_name as organisation_name,
        cce.profession_id as profession_id,
        cce.profession_name as profession_name,
        cce.grade_id as grade_id,
        cce.grade_name as grade_name
        from course_completion_events cce 
        where cce.user_id = %s
        AND cce.event_timestamp BETWEEN %s - INTERVAL '{interval}'
            AND %s + INTERVAL '{interval}'
        order by abs(extract(epoch from (cce.event_timestamp - %s)))
        limit 1;
        """;

    with PostgresConnection.get_connection() as connection:
        with connection.cursor() as cursor:
            dt = DateUtil.get_as_datetime(date)
            cursor.execute(sql_query, (learner_id, dt, dt, dt,))
            result = cursor.fetchone()
            return result
    
def insert_course_completion_events(events):
    with PostgresConnection.get_connection() as connection:
        with connection.cursor() as cursor:
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
            
            try:
                rows = [(event["external_id"], event["user_id"], event["user_email"], event["course_id"], event["course_title"], event["event_timestamp"], event["organisation_id"], event["profession_id"], event["grade_id"], event["grade_name"], event["profession_name"], event["organisation_name"],) for event in events]
                cursor.executemany(insert_query, rows)
                connection.commit()
            except Exception as e:
                print(f"Error inserting course completion events: {e}")
                connection.rollback()
                raise e
            
def delete_course_completion_events_by_external_ids(external_ids):
    with PostgresConnection.get_connection() as connection:
        with connection.cursor() as cursor:
            query = """DELETE FROM course_completion_events 
                WHERE external_id = ANY(%s);"""
            cursor.execute(query, (external_ids,))
            connection.commit()
            return cursor.rowcount