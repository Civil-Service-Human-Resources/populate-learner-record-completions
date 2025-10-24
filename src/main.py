import LearnerRecordClient
import LearningCatalogueClient
import LearningPeriodUtil
from datetime import datetime

courses = LearningCatalogueClient.get_all_courses()
print("Total courses:", len(courses))

completions = LearnerRecordClient.get_last_completions("2025-10-21", "2025-10-23")
print("Total completions:", len(completions))

for completion in completions:
    user_id = completion[0]
    organisation_code = completion[1]
    course_id = completion[2]
    last_completion_date = completion[3]

    course = next((c for c in courses if c["id"] == course_id), None)
    audiences = course["audiences"] if course else []
    audience_for_users_organisation = next((audience for audience in audiences if organisation_code in audience["departments"]), None)
    start_of_learning_period = datetime.strptime("1970-01-01", "%Y-%m-%d")
    if audience_for_users_organisation and "requiredBy" in audience_for_users_organisation and "frequency" in audience_for_users_organisation:
        frequency = audience_for_users_organisation["frequency"]
        start_of_learning_period = LearningPeriodUtil.get_current_learning_period(audience_for_users_organisation["requiredBy"], frequency)

        completed_courses_without_lr_register = LearnerRecordClient.get_user_ids_and_course_ids_for_completed_courses_not_registered_in_learner_record(
            course_id,
            start_of_learning_period,
            len([m for m in course["modules"] if m["optional"] == False]),
            datetime.strptime("2025-10-21", "%Y-%m-%d")
        )

        print(completed_courses_without_lr_register)
        
        

