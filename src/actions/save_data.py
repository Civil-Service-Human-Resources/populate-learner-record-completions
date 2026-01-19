import modules.learnerRecord.LearnerRecordDAO as LearnerRecordDAO
import pickle
import modules.learningCatalogue.LearningCatalogueDAO as LearningCatalogueDAO
import modules.csrs.CsrsService as CsrsService
import modules.reporting.ReportingDAO as ReportingDAO
import os
import sys

# Define the date range:
start_date = '2022-01-01T00:00:00'
end_date = '2026-01-15T23:59:59'

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
    save_learner_completions_from_reporting([record[0] for record in last_mandatory_module_completions])
    

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


run()
