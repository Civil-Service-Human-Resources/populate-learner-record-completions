import modules.learner.LearnerService as LearnerService
from datetime import datetime
def test_get_learner_details_returns_learner_details_from_reporting_if_found(mocker):
    learner_details_from_reporting = ('learner1-reporting@cabinetoffice.gov.uk', 1, 'Cabinet Office', 5, 'Analysis', 5, 'Grade 7')
    learner_details_from_csrs = ('learner1-csrs@cabinetoffice.gov.uk', 1, 'Cabinet Office', 5, 'Analysis', 5, 'Grade 7')

    mocker.patch.object(LearnerService.ReportingAppDataDAO, 'get_reporting_data_for_user_and_date', return_value=learner_details_from_reporting)
    mocker.patch.object(LearnerService.CsrsService, 'get_current_learner_details', return_value=learner_details_from_csrs)
    mocker.patch.object(LearnerService.CsrsService, 'get_organisation_by_id')
    mocker.patch.object(LearnerService.CsrsService, 'get_organisation_hierarchy')

    details = LearnerService.get_learner_details("abc123", "2025-01-01T00:00:00")
    assert details['user_email'] == 'learner1-reporting@cabinetoffice.gov.uk'
    assert details["organisation_id"] == 1
    assert details["organisation_name"] == "Cabinet Office"
    assert details["profession_id"] == 5
    assert details["profession_name"] == 'Analysis'
    assert details["grade_id"] == 5
    assert details["grade_name"] == 'Grade 7'

def test_get_learner_details_returns_learner_details_from_csrs_if_not_found_from_reporting_but_found_from_csrs(mocker):
    learner_details_from_reporting = None
    learner_details_from_csrs = ('learner1-csrs@cabinetoffice.gov.uk', 1, 'Cabinet Office', 5, 'Analysis', 5, 'Grade 7')
    mocker.patch.object(LearnerService.CsrsService, 'get_organisation_hierarchy')
    mocker.patch.object(LearnerService.ReportingAppDataDAO, 'get_reporting_data_for_user_and_date', return_value=learner_details_from_reporting)
    mocker.patch.object(LearnerService.CsrsService, 'get_current_learner_details', return_value=learner_details_from_csrs)
    mocker.patch.object(LearnerService.CsrsService, 'get_organisation_by_id')


    details = LearnerService.get_learner_details("abc123", "2025-01-01T00:00:00")
    assert details['user_email'] == 'learner1-csrs@cabinetoffice.gov.uk'
    assert details["organisation_id"] == 1
    assert details["organisation_name"] == "Cabinet Office"
    assert details["profession_id"] == 5
    assert details["profession_name"] == 'Analysis'
    assert details["grade_id"] == 5
    assert details["grade_name"] == 'Grade 7'

def test_get_learner_details_returns_None_not_found_from_reporting_or_csrs(mocker):
    learner_details_from_reporting = None
    learner_details_from_csrs = None

    mocker.patch.object(LearnerService.ReportingAppDataDAO, 'get_reporting_data_for_user_and_date', return_value=learner_details_from_reporting)
    mocker.patch.object(LearnerService.CsrsService, 'get_current_learner_details', return_value=learner_details_from_csrs)
    mocker.patch.object(LearnerService.CsrsService, 'get_organisation_by_id')

    details = LearnerService.get_learner_details("abc123", "2025-01-01T00:00:00")
    assert details is None

def test_get_learner_details_returns_correct_learner_details_for_completion_date_from_reporting(mocker):
    completion_date = '2025-01-01T00:00:00'

    reporting_data = [
        ('u1', 'user1@domain.gov.uk', 1, 'Cabinet Office', 1, 'Analysis', 5, 'Grade 7', datetime(2024, 1, 12, 15, 8)),
        ('u2', 'user2@domain.gov.uk', 1, 'Cabinet Office', 1, 'Analysis', 5, 'Grade 7', datetime(2024, 5, 12, 15, 8)),
        ('u1', 'user1@domain.gov.uk', 1, 'Cabinet Office', 1, 'Analysis', 5, 'Grade 7', datetime(2024, 8, 12, 15, 8)),
        ('u1', 'user1@domain.gov.uk', 1, 'Cabinet Office', 1, 'Analysis', 5, 'Grade 7', datetime(2024, 10, 1, 15, 8)),
        ('u1', 'user1@domain.gov.uk', 1, 'Cabinet Office', 1, 'Analysis', 5, 'Grade 7', datetime(2024, 12, 1, 15, 8))
    ]

    mocker.patch.object(LearnerService.ReportingAppDataDAO, 'get_reporting_data', return_value=reporting_data)
    mocker.patch.object(LearnerService.CsrsService, 'get_current_learner_details')
    mocker.patch.object(LearnerService.CsrsService, 'get_organisation_by_id', return_value=(1, None, '1', 'CO', 'Cabinet Office', 'PURCHASE_ORDER', None, datetime(2023, 11, 8, 14, 41, 28), datetime(2025, 11, 4, 12, 51, 55)))
    mocker.patch.object(LearnerService.CsrsService, 'get_organisation_hierarchy', return_value=[(1, None, '1', 'CO', 'Cabinet Office', 'PURCHASE_ORDER', None, datetime(2023, 11, 8, 14, 41, 28), datetime(2025, 11, 4, 12, 51, 55))])

    learner_details = LearnerService.get_learner_details('u1', completion_date)
    
    assert learner_details["user_email"] == "user1@domain.gov.uk"
    assert learner_details["organisation_id"] == 1
    assert learner_details["organisation_name"] == 'Cabinet Office'
    assert learner_details["profession_id"] == 1
    assert learner_details["profession_name"] == 'Analysis'
    assert learner_details["grade_id"] == 5
    assert learner_details["grade_name"] == 'Grade 7'
