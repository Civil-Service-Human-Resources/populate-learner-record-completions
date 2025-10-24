import mysql.connector
import config

mysql_config = config.get_config()["mysql"]

db = mysql.connector.connect(
  host = mysql_config["host"],
  user= mysql_config["username"],
  password= mysql_config["password"]
)

def get_module_record(user_id, course_id):
    cursor = db.cursor()
    query = "SELECT * FROM learner_record.module_record WHERE user_id = %s AND course_id = %s"
    cursor.execute(query, (user_id, course_id,))
    result = cursor.fetchall()
    cursor.close()
    return result

def get_last_completions(from_date, to_date):
    cursor = db.cursor()
    query = """select * from (
select mr.user_id, ou.code, mr.course_id, max(mr.completion_date) as last_completion_date from learner_record.module_record mr
    join csrs.`identity` i on i.uid = mr.user_id
    join csrs.civil_servant cs on cs.identity_id = i.id
    join csrs.organisational_unit ou on ou.id = cs.organisational_unit_id
    group by mr.user_id
    order by last_completion_date desc
) as last_completions
where last_completions.last_completion_date between %s and %s"""
    cursor.execute(query, (from_date, to_date,))
    result = cursor.fetchall()
    cursor.close()
    return result

def get_user_ids_and_course_ids_for_completed_courses_not_registered_in_learner_record(course_id, start_of_learning_period, number_of_mandatory_courses_in_course, date_of_course_completion_from):
    cursor = db.cursor()
    query = """select learner_id, resource_id from learner_record.learner_records lr
            left join learner_record.learner_record_events lre on lre.learner_record_id = lr.id
            where lre.id is null
            and lr.resource_id = %s
            and lr.learner_id in (select data.user_id  from (
            select mr.user_id, count(state) as completed_courses, max(mr.completion_date) as last_completed from learner_record.module_record mr 
                where mr.course_id = %s
                and state = 'COMPLETED'
                and optional = 0
                and mr.completion_date >= %s
                group by mr.user_id
        ) as data
        where data.completed_courses = %s
        and data.last_completed >= %s)
        order by lr.created_timestamp desc"""
    cursor.execute(query, (course_id, course_id, start_of_learning_period, number_of_mandatory_courses_in_course, date_of_course_completion_from,))
    result = cursor.fetchall()
    cursor.close()
    return result