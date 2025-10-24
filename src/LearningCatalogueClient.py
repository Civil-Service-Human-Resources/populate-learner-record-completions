from elasticsearch import Elasticsearch
import config

elasticsearch_config = config.get_config()["elasticsearch"]

es = Elasticsearch(
    elasticsearch_config["host"],
    basic_auth=(elasticsearch_config["username"], elasticsearch_config["password"]),
    verify_certs=True
)

def get_all_courses():
    results = es.search(index="courses", body={"query": {"match_all": {}}}, size=10000)["hits"]["hits"]
    return [result["_source"] for result in results]

def get_course(course_id):
    return es.get(index="courses", id=course_id)["_source"]