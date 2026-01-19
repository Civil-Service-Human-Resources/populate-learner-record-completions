
import modules.csrs.CsrsService as CsrsService
import modules.reporting.ReportingAppDataDAO as ReportingAppDataDAO

def get_learner_details(user_id: str, completion_date: str):
  reporting_data = ReportingAppDataDAO.get_reporting_data_for_user_and_date(user_id, completion_date)

  if reporting_data is not None:
    learner_data = reporting_data
  else:
    csrs_data = CsrsService.get_current_learner_details(user_id)
    learner_data = csrs_data

  if learner_data is None:
    return None

  learner_details = {
    "user_email": learner_data[0],
    "organisation_id": learner_data[1],
    "organisation_name": learner_data[2],
    "profession_id": learner_data[3],
    "profession_name": learner_data[4],
    "grade_id": learner_data[5],
    "grade_name": learner_data[6]
  }

  organisation = CsrsService.get_organisation_by_id(learner_details["organisation_id"])
  organisation_hierarchy = CsrsService.get_organisation_hierarchy(organisation[2])
  hierarchy_names = [org[4] for org in organisation_hierarchy]
  hierarchy_names.reverse()
  learner_details["organisation_hierarchy"] = " | ".join(hierarchy_names)

  print(learner_details)
  return learner_details