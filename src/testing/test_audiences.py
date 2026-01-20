import modules.audience.AudienceService as AudienceService
import datetime

def test_get_audience_for_organisation_returns_none_if_no_audiences_is_None():
    organisation_id = 1
    audiences = None

    audience = AudienceService.get_audience_for_organisation(audiences, organisation_id)

    assert audience is None

def test_get_audience_for_organisation_returns_none_if_no_audiences_is_empty():
    organisation_id = 1
    audiences = []

    audience = AudienceService.get_audience_for_organisation(audiences, organisation_id)

    assert audience is None

def test_get_audience_returns_none_if_no_mandatory_audiences_present():
    audiences = [
        {
            'areasOfWork': [], 
            'id': 'audience1',
            'eventId': None, 
            'requiredBy': None, 
            'name': 'Audience1', 
            'departments': ['p64'], 
            'grades': ['PS'], 
            'interests': ['Leadership'], 
            'type': 'OPEN', 
            'frequency': None
         },
         {
            'areasOfWork': [], 
            'id': 'audience2',
            'eventId': None, 
            'requiredBy': None, 
            'name': 'Audience2', 
            'departments': ['p64'], 
            'grades': ['PS'], 
            'interests': ['Leadership'], 
            'type': 'OPEN', 
            'frequency': None
         }
    ]
    organisation_id = 1

    audience = AudienceService.get_audience_for_organisation(audiences, organisation_id)
    assert audience is None

def test_get_audience_returns_none_if_no_audiences_with_requiredBy_present():
    audiences = [
        {
            'areasOfWork': [], 
            'id': 'audience1',
            'eventId': None, 
            'requiredBy': None, 
            'name': 'Audience1', 
            'departments': ['p64'], 
            'grades': ['PS'], 
            'interests': ['Leadership'], 
            'type': 'REQUIRED_LEARNING', 
            'frequency': None
         },
         {
            'areasOfWork': [], 
            'id': 'audience2',
            'eventId': None, 
            'name': 'Audience2', 
            'departments': ['p64'], 
            'grades': ['PS'], 
            'interests': ['Leadership'], 
            'type': 'REQUIRED_LEARNING', 
            'frequency': None
         }
    ]
    organisation_id = 1

    audience = AudienceService.get_audience_for_organisation(audiences, organisation_id)
    assert audience is None


def test_get_audience_returns_audience_if_audience_department_matches_learner_department(mocker):

    audiences = [
        {
            'areasOfWork': [], 
            'id': 'audience1',
            'eventId': None, 
            'name': 'Audience1', 
            'departments': ['CO1', 'OTHERORG'], 
            'grades': [], 
            'interests': [], 
            'type': 'REQUIRED_LEARNING', 
            'requiredBy': '2025-01-01T00:00:00',
            'frequency': 'P1Y'
         }
    ]
    organisation_id = 1

    mock_organisations = [(1, None, 'CO1', 'CO', 'Cabinet Office', 'PURCHASE_ORDER', None, datetime.datetime(2023, 11, 8, 14, 41, 28), datetime.datetime(2025, 11, 4, 12, 51, 55))]

    mocker.patch.object(AudienceService.CsrsService, 'get_organisation_hierarchy_by_id', return_value=mock_organisations)

    audience = AudienceService.get_audience_for_organisation(audiences, organisation_id)
    assert audience is not None
    assert audience['id'] == 'audience1'
    
def test_get_audience_returns_audience_if_audience_department_matches_learner_department_parent_department(mocker):
    audiences = [
        {
            'areasOfWork': [], 
            'id': 'audience1',
            'eventId': None, 
            'name': 'Audience1', 
            'departments': ['CO1'], 
            'grades': [], 
            'interests': [], 
            'type': 'REQUIRED_LEARNING', 
            'requiredBy': '2025-01-01T00:00:00',
            'frequency': 'P1Y'
         }
    ]
    organisation_id = 244

    mock_organisations = [
        (244, 1, 'CO-SUB', 'CO-SUB', 'CO Suborg', 'PURCHASE_ORDER', None, datetime.datetime(2023, 11, 8, 14, 41, 28), datetime.datetime(2025, 12, 3, 11, 55, 43)), 
        (1, None, 'CO1', 'CO', 'Cabinet Office', 'PURCHASE_ORDER', None, datetime.datetime(2023, 11, 8, 14, 41, 28), datetime.datetime(2025, 11, 4, 12, 51, 55))]

    mocker.patch.object(AudienceService.CsrsService, 'get_organisation_hierarchy_by_id', return_value=mock_organisations)

    audience = AudienceService.get_audience_for_organisation(audiences, organisation_id)
    assert audience is not None
    assert audience['id'] == 'audience1'

def test_get_audience_returns_None_if_learner_department_is_different_from_audience_departments(mocker): 
    audiences = [
        {
            'areasOfWork': [], 
            'id': 'audience1',
            'eventId': None, 
            'name': 'Audience1', 
            'departments': ['ORG2', 'ORG3'], 
            'grades': [], 
            'interests': [], 
            'type': 'REQUIRED_LEARNING', 
            'requiredBy': '2025-01-01T00:00:00',
            'frequency': 'P1Y'
         }
    ]
    organisation_id = 1

    mock_organisations = [(1, None, 'CO1', 'CO', 'Cabinet Office', 'PURCHASE_ORDER', None, datetime.datetime(2023, 11, 8, 14, 41, 28), datetime.datetime(2025, 11, 4, 12, 51, 55))]

    mocker.patch.object(AudienceService.CsrsService, 'get_organisation_hierarchy_by_id', return_value=mock_organisations)

    audience = AudienceService.get_audience_for_organisation(audiences, organisation_id)
    assert audience is None