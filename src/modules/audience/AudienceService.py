import modules.learningCatalogue.LearningCatalogueAppDataDAO as LearningCatalogueAppDataDAO
import modules.csrs.CsrsService as CsrsService

def get_audience(learner, course_id):
    audiences = next(c for c in LearningCatalogueAppDataDAO.get_all_courses() if c["id"] == course_id)["audiences"]
    if len(audiences) == 0:
        return None
    
    grade = CsrsService.get_grade_by_id(learner["grade_id"])
    organisation_hierarchy = CsrsService.get_organisation_hierarchy_by_id(learner["organisation_id"])
    
    if len([a for a in audiences if "requiredBy" in a and a["requiredBy"] is not None]) == 0:
        return None
    
    filtered_audiences = audiences
    for audience in audiences:
        if audience["type"] == "OPEN":
            filtered_audiences.remove(audience)
            break

        if len(audience["areasOfWork"]) > 0 and learner["profession_name"] not in audience["areasOfWork"]:
            filtered_audiences.remove(audience)
            break

        if len(audience["grades"]) > 0 and grade[2] not in audience["grades"]:
            filtered_audiences.remove(audience)
            break

        if len(audience["departments"]) > 0:
            organisation_audiences = []
            for organisation in organisation_hierarchy:
                print("Organisation:", organisation)
                if organisation[2] in audience["departments"]:
                    organisation_audiences.append(audience)
                    break

            if len(organisation_audiences) == 0:
                filtered_audiences.remove(audience)
                break

    return len(filtered_audiences) > 0 and filtered_audiences[0] or None