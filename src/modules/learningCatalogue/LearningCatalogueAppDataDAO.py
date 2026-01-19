import pickle

def get_all_courses():
    with open("/app-data/courses.pkl", "rb") as f:
        courses = pickle.load(f)
    return courses