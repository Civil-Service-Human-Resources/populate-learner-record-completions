import modules.database.MySQLConnection as MySQLConnection

def get_all_organisations():
  with MySQLConnection.get_connection() as connection:
      with connection.cursor() as cursor:
        query = "SELECT * FROM csrs.organisational_unit"
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result
      
def get_all_grades():
  with MySQLConnection.get_connection() as connection:
      with connection.cursor() as cursor:
        query = "SELECT * FROM csrs.grade"
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result

def get_current_learner_details(uid):
  query = """select 
    i.email as user_email,
    ou.id as organisation_id,
    ou.name as organisation_name,
    p.id as profession_id,
    p.name as profession_name,
    g.id as grade_id,
    g.name as grade_name
  from
    `identity`.`identity` i 
  join
    csrs.`identity` i2 on i2.uid = i.uid 
    join csrs.civil_servant cs on cs.identity_id = i2.id 
    left join csrs.organisational_unit ou on ou.id = cs.organisational_unit_id 
    left join csrs.profession p on p.id = cs.profession_id 
    left join csrs.grade g on g.id = cs.grade_id 
  where i.uid = %s;"""
  with MySQLConnection.get_connection() as connection:
    with connection.cursor() as cursor:
      cursor.execute(query, (uid,))
      result = cursor.fetchone()
      cursor.close()
      return result