import CsrsDAO

all_organisations = CsrsDAO.get_all_organisations()

def get_organisation_hierarchy(organisation_code: str):
    organisations = []
    organisation_cursor = get_organisation_by_code(organisation_code)

    while organisation_cursor[1] is not None:
        organisations.append(organisation_cursor)
        organisation_cursor = get_organisation_by_id(organisation_cursor[1])

    organisations.append(organisation_cursor)

    return organisations
    
def get_organisation_by_code(organisation_code: str):
    organisation = next((org for org in all_organisations if org[2] == organisation_code), None)
    return organisation

def get_organisation_by_id(organisation_id: int):
    organisation = next((org for org in all_organisations if org[0] == organisation_id), None)
    return organisation