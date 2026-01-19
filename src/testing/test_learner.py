import modules.learner.LearnerService as LearnerService

def test_get_learner_details_returns_learner_details_from_reporting_if_found(mocker):
    learner_details_from_reporting = ('learner1-reporting@cabinetoffice.gov.uk', 1, 'Cabinet Office', 5, 'Analysis', 5, 'Grade 7')
    learner_details_from_csrs = ('learner1-csrs@cabinetoffice.gov.uk', 1, 'Cabinet Office', 5, 'Analysis', 5, 'Grade 7')

    mocker.patch.object(LearnerService.ReportingAppDataDAO, 'get_reporting_data_for_user_and_date', return_value=learner_details_from_reporting)
    mocker.patch.object(LearnerService.CsrsService, 'get_current_learner_details', return_value=learner_details_from_csrs)

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

    mocker.patch.object(LearnerService.ReportingAppDataDAO, 'get_reporting_data_for_user_and_date', return_value=learner_details_from_reporting)
    mocker.patch.object(LearnerService.CsrsService, 'get_current_learner_details', return_value=learner_details_from_csrs)

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

    details = LearnerService.get_learner_details("abc123", "2025-01-01T00:00:00")
    assert details is None