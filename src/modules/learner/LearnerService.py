import modules.csrs.CsrsService as CsrsService
import pandas as pd

def get_learner_details(reporting_data, csrs_data_df, user_id: str, completion_date: str):
  user_reporting_data = None

  
  try:
    filtered_df = reporting_data.loc[[(user_id)]]
    user_reporting_data = (filtered_df.assign(distance=(filtered_df["event_timestamp"] - pd.Timestamp(completion_date)).abs())
          .sort_values("distance")
          .drop(columns="distance")
      )
  except:
    user_reporting_data = None


  if user_reporting_data is not None:
    learner_data = user_reporting_data.iloc[0]
  else:
    csrs_data = CsrsService.get_current_learner_details(csrs_data_df, user_id)
    learner_data = csrs_data

  if learner_data is None:
    return None

  learner_details = {
    "user_email": learner_data["user_email"],
    "organisation_id": learner_data["organisation_id"],
    "organisation_name": learner_data["organisation_name"],
    "profession_id": learner_data["profession_id"],
    "profession_name": learner_data["profession_name"],
    "grade_id": learner_data["grade_id"],
    "grade_name": learner_data["grade_name"]
  }

  organisation_hierarchy = CsrsService.get_organisation_hierarchy_by_id(learner_details["organisation_id"])
  hierarchy_names = [org[4] for org in organisation_hierarchy]
  hierarchy_names.reverse()
  learner_details["organisation_hierarchy"] = " | ".join(hierarchy_names)

  return learner_details