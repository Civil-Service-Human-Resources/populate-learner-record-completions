import modules.learnerRecord.LearnerRecordDAO as LearnerRecordDAO
import pickle
import modules.learningCatalogue.LearningCatalogueDAO as LearningCatalogueDAO
import modules.csrs.CsrsService as CsrsService
import modules.reporting.ReportingDAO as ReportingDAO
import os
import sys

start_date = "2022-01-01T00:00:00"
end_date = "2022-12-31T00:00:00"

def run():
    arguments = sys.argv[1:]

    override = arguments[0] == "--replace" if len(arguments) > 0 else False

    if len(os.listdir("/app-data")) > 0:
        if override:
            for filename in os.listdir("/app-data"):
                os.remove(os.path.join("/app-data", filename))
        else:
            sys.exit("Data already exists in the `/app-data` directory. Use --replace to overwrite the data. Example: `python save_data.py --replace`")

    save_courses()
    save_organisations()
    save_grades()
    last_mandatory_module_completions = save_last_mandatory_module_completions()
    learner_ids = list(set([record[0] for record in last_mandatory_module_completions]))


    save_learner_completions_from_reporting(learner_ids)
    save_mandatory_module_completions_for_users(learner_ids)
    save_learner_record_course_completion_events(learner_ids)
    save_csrs_learner_details(learner_ids)
    
def save_courses():
    courses = LearningCatalogueDAO.get_all_courses()
    pickle.dump(courses, open("/app-data/courses.pkl", "wb"))
    print(f"Saved {len(courses)} courses")

def save_organisations():
    organisations = CsrsService.get_all_organisations()
    pickle.dump(organisations, open("/app-data/organisations.pkl", "wb"))
    print(f"Saved {len(organisations)} organisations")

def save_grades():
    grades = CsrsService.get_all_grades()
    pickle.dump(grades, open("/app-data/grades.pkl", "wb"))
    print(f"Saved {len(grades)} grades")

def save_last_mandatory_module_completions():
    last_mandatory_module_completions = LearnerRecordDAO.get_last_mandatory_module_completions(start_date, end_date)
    pickle.dump(last_mandatory_module_completions, open("/app-data/last_mandatory_module_completions.pkl", "wb"))
    print(f"Saved {len(last_mandatory_module_completions)} module completions")
    return last_mandatory_module_completions

def save_learner_completions_from_reporting(learner_ids):
    completions = list(ReportingDAO.get_completions_for_learners(learner_ids, start_date, end_date))
    pickle.dump(completions, open("/app-data/reporting_completions.pkl", "wb"))
    print(f"Saved {len(completions)} learner completions from reporting")
    return completions

def save_mandatory_module_completions_for_users(learner_ids):
    print("Saving mandatory module completions")
    module_completions = LearnerRecordDAO.get_required_module_completions(learner_ids)
    pickle.dump(module_completions, open("/app-data/learner_record_module_completions.pkl", "wb"))
    print(f"Saved {len(module_completions)} module completions from learner record")

def save_learner_record_course_completion_events(learner_ids):
    completion_events = LearnerRecordDAO.get_learner_record_course_completion_events_for_users(learner_ids)
    pickle.dump(completion_events, open("/app-data/learner_record_course_completion_events.pkl", "wb"))
    print(f"Saved {len(completion_events)} course completion events")

def save_csrs_learner_details(learner_ids):
    details = CsrsService.get_learners_details(learner_ids)
    pickle.dump(details, open("/app-data/csrs_learners_details.pkl", "wb"))

run()
