from datetime import datetime
import modules.database.MySQLConnection as MySQLConnection

def get_required_module_completions_for_user_and_course(user_id, course_id, starting_date, ending_date=datetime.now().strftime("%Y-%m-%d %H:%M")):
    with MySQLConnection.get_connection() as connection:
        with connection.cursor() as cursor:
            query = """SELECT * FROM learner_record.module_record 
                WHERE user_id = %s
                AND course_id = %s
                and optional = 0
                and state = 'COMPLETED'
                and completion_date between %s and %s
                order by completion_date asc;"""
            cursor.execute(query, (user_id, course_id, starting_date, ending_date,))
            result = cursor.fetchall()
            return result

def get_last_mandatory_module_completions(from_date, to_date=datetime.now().strftime("%Y-%m-%dT%H:%M")):
    with MySQLConnection.get_connection() as connection:
        with connection.cursor() as cursor:
            query = """select mr.user_id, ou.code, mr.course_id, max(mr.completion_date)as last_completion_date, mr.created_at from learner_record.module_record mr
                join csrs.`identity` i on i.uid = mr.user_id
                join csrs.civil_servant cs on cs.identity_id = i.id
                join csrs.organisational_unit ou on ou.id = cs.organisational_unit_id
                where mr.state = 'COMPLETED' and mr.optional = 0
                and mr.completion_date between %s and %s
                group by mr.user_id, mr.course_id
                order by last_completion_date asc;"""
            cursor.execute(query, (from_date, to_date,))
            result = cursor.fetchall()
            return result

def get_course_completion_events(user_id, course_id, from_date, to_date):
    with MySQLConnection.get_connection() as connection:
        with connection.cursor() as cursor:
            query = """select * from learner_record.learner_record_events lre
            where lre.learner_record_id = (select id from learner_record.learner_records lr where lr.learner_id = %s and lr.resource_id = %s)
            and lre.event_timestamp >= %s
            and lre.event_timestamp <= %s
            and lre.learner_record_event_type = 4;"""
            cursor.execute(query, (user_id, course_id, from_date, to_date,))
            result = cursor.fetchall()
            return result

def insert_learner_record_events(rows):
    with MySQLConnection.get_connection() as connection:
        with connection.cursor() as cursor:
            apply_results = []
            for row in rows:
                try:
                    learner_id = row["learner_id"]
                    resource_id = row["resource_id"]
                    event_timestamp = row["event_timestamp"]

                    sql_query = """insert into learner_record.learner_record_events 
                        (learner_record_id, learner_record_event_type, learner_record_event_source, event_timestamp)
                        select lr.id,4,1,%s from learner_record.learner_records lr 
                        where lr.learner_id = %s and lr.resource_id = %s;"""
                    
                    cursor.execute(sql_query, (event_timestamp, learner_id, resource_id,))
                    connection.commit()
                    applied_successfully = True
                except:
                    connection.rollback()
                    applied_successfully = False

                apply_results.append({
                    "applied_successfully": applied_successfully,
                    "rows_added": cursor.rowcount if applied_successfully else 0,
                    "row_id": cursor.lastrowid,
                    "row_data": row
                })

            return apply_results

def insert_learner_record_events_in_batches(rows, batch_size=100):
    select_statement = "select lr.id,4,1,%s from learner_record.learner_records lr where lr.learner_id = %s and lr.resource_id = %s"

    batch_start_index = list(range(0, len(rows), batch_size))

    apply_results = []
    
    for start_index in batch_start_index:
        row_batch = rows[start_index : start_index + batch_size]
        with MySQLConnection.get_connection() as connection:
            with connection.cursor() as cursor:
                params = []
                try:
                    for row in row_batch:
                        
                        learner_id = row["learner_id"]
                        resource_id = row["resource_id"]
                        event_timestamp = row["event_timestamp"]
                        params.extend([event_timestamp, learner_id, resource_id])

                    select_statements = " union all ".join([select_statement] * len(row_batch))

                    sql_query = f"""insert into learner_record.learner_record_events 
                        (learner_record_id, learner_record_event_type, learner_record_event_source, event_timestamp)
                        {select_statements};"""
                    
                    cursor.execute(sql_query, params)
                    connection.commit()
                    applied_successfully = True
                except:
                    connection.rollback()
                    applied_successfully = False
                finally:
                    cursor.close()

                apply_results.append({
                    "applied_successfully": applied_successfully,
                    "rows_added": cursor.rowcount if applied_successfully else 0,
                    "start_index": start_index
                })

    return apply_results

def delete_learner_record_events_by_ids(event_ids):
    placeholders = ','.join(['%s'] * len(event_ids))
    with MySQLConnection.get_connection() as connection:
        with connection.cursor() as cursor:
            query = f"""DELETE FROM learner_record.learner_record_events 
                WHERE id in ({placeholders});"""
            cursor.execute(query, event_ids)
            connection.commit()
            return cursor.rowcount