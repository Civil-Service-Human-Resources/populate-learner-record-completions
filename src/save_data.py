import LearnerRecordDAO
import pickle
import LearningCatalogueDAO
import CsrsDAO
import os

os.mkdir("data")

courses = LearningCatalogueDAO.get_all_courses()
pickle.dump(courses, open("data/courses.pkl", "wb"))
print(f"Saved {len(courses)} courses")

last_mandatory_module_completions = LearnerRecordDAO.get_last_mandatory_module_completions(from_date='2025-04-01 15:00:00')
pickle.dump(last_mandatory_module_completions, open("data/last_mandatory_module_completions.pkl", "wb"))
print(f"Saved {len(last_mandatory_module_completions)} module completions")

organisations = CsrsDAO.get_all_organisations()
pickle.dump(organisations, open("data/organisations.pkl", "wb"))
print(f"Saved {len(organisations)} organisations")