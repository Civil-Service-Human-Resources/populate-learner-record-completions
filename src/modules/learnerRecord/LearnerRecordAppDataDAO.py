import pickle

def get_last_mandatory_module_completions():
    return pickle.load(open("/app-data/last_mandatory_module_completions.pkl", "rb"))