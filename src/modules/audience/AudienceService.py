import modules.csrs.CsrsService as CsrsService

def get_audience_for_organisation(audiences, organisation_id):
    if audiences == None or len(audiences) == 0:
        return None
    
    if len([a for a in audiences if "requiredBy" in a and a["requiredBy"] is not None]) == 0:
        return None
    
    organisation_hierarchy = CsrsService.get_organisation_hierarchy_by_id(organisation_id)
    organisation_codes = [organisation[2] for organisation in organisation_hierarchy]

    for organisation_code in organisation_codes:
        audience_for_organisation_code = next((audience for audience in audiences if organisation_code in audience["departments"]), None)
        if audience_for_organisation_code is not None:
            return audience_for_organisation_code