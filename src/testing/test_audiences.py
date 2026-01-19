import modules.audience.AudienceService as AudienceService
import datetime
def test_get_audience_returns_none_if_no_audiences_present_in_course(mocker):
    fake_courses = [{
        "id": "course_1",
        "audiences": []
    }]

    mocker.patch.object(AudienceService.LearningCatalogueAppDataDAO, 'get_all_courses', return_value=fake_courses)

    learner = {}
    audience = AudienceService.get_audience(learner, "course_1")
    assert audience is None

def test_get_audience_returns_none_if_no_mandatory_audiences_present(mocker):
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
    fake_courses = [{
        "id": "course_1",
        "audiences": audiences
    }]

    mocker.patch.object(AudienceService.LearningCatalogueAppDataDAO, 'get_all_courses', return_value=fake_courses)

    learner = {}
    audience = AudienceService.get_audience(learner, "course_1")
    assert audience is None

def test_get_audience_returns_none_if_no_audiences_with_requiredBy_present(mocker):
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
    fake_courses = [{
        "id": "course_1",
        "audiences": audiences
    }]

    mocker.patch.object(AudienceService.LearningCatalogueAppDataDAO, 'get_all_courses', return_value=fake_courses)

    learner = {}
    audience = AudienceService.get_audience(learner, "course_1")
    assert audience is None

def test_get_audience_returns_audience_when_areas_of_work_match_learners_profession(mocker):
    audiences1 = [
        {
            'areasOfWork': ['AreaOfWork1'], 
            'id': 'audience1',
            'eventId': None, 
            'name': 'Audience1', 
            'departments': [], 
            'grades': [], 
            'interests': [], 
            'type': 'REQUIRED_LEARNING', 
            'requiredBy': '2025-01-01T00:00:00',
            'frequency': 'P1Y'
         },
        {
            'areasOfWork': ["AreaOfWork2"], 
            'id': 'audience2',
            'eventId': None, 
            'name': 'Audience2', 
            'departments': [], 
            'grades': [], 
            'interests': [], 
            'type': 'REQUIRED_LEARNING', 
            'requiredBy': '2025-01-01T00:00:00',
            'frequency': 'P1Y'
         },
    ]
    fake_courses = [{
        "id": "course_1",
        "audiences": audiences1
    }]

    learner = {
        "profession_name": "AreaOfWork1"
    }

    mocker.patch.object(AudienceService.LearningCatalogueAppDataDAO, 'get_all_courses', return_value=fake_courses)
    audience = AudienceService.get_audience(learner, "course_1")
    assert audience is not None
    assert audience['id'] == 'audience1'

def test_get_audience_returns_None_when_areas_of_work_do_not_match_learners_profession(mocker):
    audiences2 = [
        {
            'areasOfWork': ['AreaOfWork1'], 
            'id': 'audience1',
            'eventId': None, 
            'name': 'Audience1', 
            'departments': [], 
            'grades': [], 
            'interests': [], 
            'type': 'REQUIRED_LEARNING', 
            'requiredBy': '2025-01-01T00:00:00',
            'frequency': 'P1Y'
         },
        {
            'areasOfWork': ['AreaOfWork2'], 
            'id': 'audience2',
            'eventId': None, 
            'name': 'Audience2', 
            'departments': [], 
            'grades': [], 
            'interests': [], 
            'type': 'REQUIRED_LEARNING', 
            'requiredBy': '2025-01-01T00:00:00',
            'frequency': 'P1Y'
         },
    ]
    fake_courses = [{
        "id": "course_1",
        "audiences": audiences2
    }]

    learner = {
        "profession_name": "AreaOfWork3"
    }

    mocker.patch.object(AudienceService.LearningCatalogueAppDataDAO, 'get_all_courses', return_value=fake_courses)
    audience = AudienceService.get_audience(learner, "course_1")
    assert audience is None

def test_get_audience_returns_audience_when_grade_matches_learners_grade(mocker):
    audiences1 = [
        {
            'areasOfWork': [], 
            'id': 'SEOAudience',
            'eventId': None, 
            'name': 'Audience1', 
            'departments': [], 
            'grades': ['SEO'], 
            'interests': [], 
            'type': 'REQUIRED_LEARNING', 
            'requiredBy': '2025-01-01T00:00:00',
            'frequency': 'P1Y'
         },
        {
            'areasOfWork': [], 
            'id': 'Grade7Audience',
            'eventId': None, 
            'name': 'Audience2', 
            'departments': [], 
            'grades': ['Grade 7'], 
            'interests': [], 
            'type': 'REQUIRED_LEARNING', 
            'requiredBy': '2025-01-01T00:00:00',
            'frequency': 'P1Y'
         },
    ]
    fake_courses = [{
        "id": "course_1",
        "audiences": audiences1
    }]

    learner = {
        "grade_id": 1
    }

    fake_grades = [(1, None, 'SEO', 'Senior executive officer'), (2, None, 'G7', 'Grade 7')]

    mocker.patch.object(AudienceService.LearningCatalogueAppDataDAO, 'get_all_courses', return_value=fake_courses)
    mocker.patch.object(AudienceService.CsrsService.CsrsAppDataDAO, 'get_all_grades', return_value=fake_grades)

    audience = AudienceService.get_audience(learner, "course_1")
    assert audience is not None
    assert audience['id'] == 'SEOAudience'

def test_get_audience_returns_audience_when_grade_is_empty_in_audience(mocker):
    audiences = [
        {
            'areasOfWork': [], 
            'id': 'audience1',
            'eventId': None, 
            'name': 'Audience1', 
            'departments': [], 
            'grades': [], 
            'interests': [], 
            'type': 'REQUIRED_LEARNING', 
            'requiredBy': '2025-01-01T00:00:00',
            'frequency': 'P1Y'
         }
    ]
    fake_courses = [{
        "id": "course_1",
        "audiences": audiences
    }]

    learner = {
        "grade_id": 1
    }

    fake_grades = [(1, None, 'SEO', 'Senior executive officer'), (2, None, 'G7', 'Grade 7')]

    mocker.patch.object(AudienceService.LearningCatalogueAppDataDAO, 'get_all_courses', return_value=fake_courses)
    mocker.patch.object(AudienceService.CsrsService.CsrsAppDataDAO, 'get_all_grades', return_value=fake_grades)

    audience = AudienceService.get_audience(learner, "course_1")
    assert audience is not None
    assert audience['id'] == 'audience1'

def test_get_audience_returns_audience_when_learner_has_no_grade(mocker):
    audiences = [
        {
            'areasOfWork': [], 
            'id': 'audience1',
            'eventId': None, 
            'name': 'Audience1', 
            'departments': [], 
            'grades': ['SEO'], 
            'interests': [], 
            'type': 'REQUIRED_LEARNING', 
            'requiredBy': '2025-01-01T00:00:00',
            'frequency': 'P1Y'
         }
    ]
    fake_courses = [{
        "id": "course_1",
        "audiences": audiences
    }]

    learner = {
        "grade_id": None
    }

    mocker.patch.object(AudienceService.LearningCatalogueAppDataDAO, 'get_all_courses', return_value=fake_courses)

    audience = AudienceService.get_audience(learner, "course_1")
    assert audience is not None
    assert audience['id'] == 'audience1'


def test_get_audience_returns_audience_if_audience_department_matches_learner_department(mocker):
    learner = {
        "organisation_id": 1
    }

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
    fake_courses = [{
        "id": "course_1",
        "audiences": audiences
    }]

    fake_organisations = [(1, None, 'CO1', 'CO', 'Cabinet Office', 'PURCHASE_ORDER', None, datetime.datetime(2023, 11, 8, 14, 41, 28), datetime.datetime(2025, 11, 4, 12, 51, 55))]

    mocker.patch.object(AudienceService.LearningCatalogueAppDataDAO, 'get_all_courses', return_value=fake_courses)
    mocker.patch.object(AudienceService.CsrsService, 'get_organisation_hierarchy_by_id', return_value=fake_organisations)

    audience = AudienceService.get_audience(learner, "course_1")
    assert audience is not None
    assert audience['id'] == 'audience1'
    
def test_get_audience_returns_audience_if_audience_department_matches_learner_department_parent_department(mocker):
    learner = {
        "organisation_id": 244
    }

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
    fake_courses = [{
        "id": "course_1",
        "audiences": audiences
    }]

    fake_organisations = [(244, 1, 'CO-SUB', 'CO-SUB', 'CO Suborg', 'PURCHASE_ORDER', None, datetime.datetime(2023, 11, 8, 14, 41, 28), datetime.datetime(2025, 12, 3, 11, 55, 43)), (1, None, 'CO1', 'CO', 'Cabinet Office', 'PURCHASE_ORDER', None, datetime.datetime(2023, 11, 8, 14, 41, 28), datetime.datetime(2025, 11, 4, 12, 51, 55))]

    mocker.patch.object(AudienceService.LearningCatalogueAppDataDAO, 'get_all_courses', return_value=fake_courses)
    mocker.patch.object(AudienceService.CsrsService, 'get_organisation_hierarchy_by_id', return_value=fake_organisations)

    audience = AudienceService.get_audience(learner, "course_1")
    assert audience is not None
    assert audience['id'] == 'audience1'

def test_get_audience_returns_None_if_learner_department_is_parent_of_audience_department(mocker):
    learner = {
        "organisation_id": 1
    }

    audiences = [
        {
            'areasOfWork': [], 
            'id': 'audience1',
            'eventId': None, 
            'name': 'Audience1', 
            'departments': ['CO-SUB'], 
            'grades': [], 
            'interests': [], 
            'type': 'REQUIRED_LEARNING', 
            'requiredBy': '2025-01-01T00:00:00',
            'frequency': 'P1Y'
         }
    ]
    fake_courses = [{
        "id": "course_1",
        "audiences": audiences
    }]

    fake_organisations = [(1, None, 'CO1', 'CO', 'Cabinet Office', 'PURCHASE_ORDER', None, datetime.datetime(2023, 11, 8, 14, 41, 28), datetime.datetime(2025, 11, 4, 12, 51, 55))]

    mocker.patch.object(AudienceService.LearningCatalogueAppDataDAO, 'get_all_courses', return_value=fake_courses)
    mocker.patch.object(AudienceService.CsrsService, 'get_organisation_hierarchy_by_id', return_value=fake_organisations)

    audience = AudienceService.get_audience(learner, "course_1")
    assert audience is None