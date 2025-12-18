import LearnerRecordDAO
import pickle
import LearningCatalogueDAO
import CsrsDAO
import os
import sys
import shutil

# Define the date range:
start_date = '2025-04-01 00:00:00'
end_date = '2025-12-31 23:59:59'

arguments = sys.argv[1:]

override = arguments[0] == "--replace" if len(arguments) > 0 else False

if os.path.exists("data") and not override:
    sys.exit("Data already exists in the `data` directory. Use --replace to overwrite the data. Example: `python save_data.py --replace`")

if os.path.exists("data"):
    shutil.rmtree("data")

os.mkdir("data")

courses = LearningCatalogueDAO.get_all_courses()
pickle.dump(courses, open("data/courses.pkl", "wb"))
print(f"Saved {len(courses)} courses")

last_mandatory_module_completions = LearnerRecordDAO.get_last_mandatory_module_completions(from_date=start_date, to_date=end_date)
pickle.dump(last_mandatory_module_completions, open("data/last_mandatory_module_completions.pkl", "wb"))
print(f"Saved {len(last_mandatory_module_completions)} module completions")

organisations = CsrsDAO.get_all_organisations()
pickle.dump(organisations, open("data/organisations.pkl", "wb"))
print(f"Saved {len(organisations)} organisations")