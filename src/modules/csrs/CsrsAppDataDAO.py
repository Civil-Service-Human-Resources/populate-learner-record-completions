import pickle

def save_organisations(organisations):
    pickle.dump(organisations, open("/app-data/organisations.pkl", "wb"))

def get_all_organisations():
    organisations = pickle.load(open("/app-data/organisations.pkl", "rb"))
    return organisations

def save_grades(grades):
    pickle.dump(grades, open("/app-data/grades.pkl", "wb"))

def get_all_grades():
    grades = pickle.load(open("/app-data/grades.pkl", "rb"))
    return grades