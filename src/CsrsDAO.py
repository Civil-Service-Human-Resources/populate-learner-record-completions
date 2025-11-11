import mysql.connector
import config
import os
import pickle

mysql_config = config.get_config()["mysql"]

db = mysql.connector.connect(
  host = mysql_config["host"],
  user= mysql_config["username"],
  password= mysql_config["password"]
)

def get_all_organisations():
    if os.path.exists("data/organisations.pkl"):
        return pickle.load(open("data/organisations.pkl", "rb"))
    else:
        cursor = db.cursor()
        query = "SELECT * FROM csrs.organisational_unit"
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        pickle.dump(result, open("data/organisations.pkl", "wb"))
        return result