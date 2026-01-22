import pickle

def get_module_completions():
    return pickle.load(open("/app-data/learner_record_module_completions.pkl", "rb"))

def get_last_mandatory_module_completions():
    return pickle.load(open("/app-data/last_mandatory_module_completions.pkl", "rb"))

def get_course_completion_events():
    return pickle.load(open("/app-data/learner_record_course_completion_events.pkl", "rb"))