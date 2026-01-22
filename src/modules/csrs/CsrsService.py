import modules.csrs.CsrsDAO as CsrsDAO
import modules.csrs.CsrsAppDataDAO as CsrsAppDataDAO

def get_organisation_hierarchy(organisation_code: str):
    organisations = []
    organisation_cursor = get_organisation_by_code(organisation_code)

    while organisation_cursor[1] is not None:
        organisations.append(organisation_cursor)
        organisation_cursor = get_organisation_by_id(organisation_cursor[1])

    organisations.append(organisation_cursor)

    return organisations

def get_organisation_hierarchy_by_id(organisation_id: int):
    organisations = []
    organisation_cursor = get_organisation_by_id(organisation_id)

    while organisation_cursor[1] is not None:
        organisations.append(organisation_cursor)
        organisation_cursor = get_organisation_by_id(organisation_cursor[1])

    organisations.append(organisation_cursor)

    return organisations
    
def get_organisation_by_code(organisation_code: str):
    all_organisations = CsrsAppDataDAO.get_all_organisations()
    organisation = next((org for org in all_organisations if org[2] == organisation_code), None)
    return organisation

def get_organisation_by_id(organisation_id: int):
    all_organisations = CsrsAppDataDAO.get_all_organisations()
    organisation = next((org for org in all_organisations if org[0] == organisation_id), None)
    return organisation

def get_grade_by_id(grade_id: int):
    all_grades = CsrsAppDataDAO.get_all_grades()
    grade = next((g for g in all_grades if g[0] == grade_id), None)
    return grade

def get_current_learner_details(all_learners_df, user_id: str):
    try:
        filtered_df = all_learners_df.loc[[(user_id)]]
        return filtered_df.iloc[0]
    except:
        return None
    

def get_all_organisations():
    return CsrsDAO.get_all_organisations()

def get_all_grades():
    return CsrsDAO.get_all_grades()

def get_learners_details(learner_ids):
    return CsrsDAO.get_learners_details(learner_ids)