import modules.csrs.CsrsService as CsrsService
import datetime

def test_get_organisation_hierarchy_by_id_returns_one_department_if_department_id_is_top_tier(mocker):
    organisation_id = 1
    mocker.patch.object(CsrsService, 'get_organisation_by_id', side_effect=get_organisation_by_id_side_effect)

    hierarchy = CsrsService.get_organisation_hierarchy_by_id(organisation_id)
    assert len(hierarchy) == 1
    assert hierarchy[0][0] == 1
    assert hierarchy[0][2] == '10211'

def test_get_organisation_hierarchy_by_id_returns_all_parent_departments_if_department_id_is_not_top_tier(mocker):
    organisation_id = 244
    mocker.patch.object(CsrsService, 'get_organisation_by_id', side_effect=get_organisation_by_id_side_effect)

    hierarchy = CsrsService.get_organisation_hierarchy_by_id(organisation_id)
    assert len(hierarchy) == 2
    assert hierarchy[0][0] == 244
    assert hierarchy[0][2] == '30440'
    assert hierarchy[1][0] == 1
    assert hierarchy[1][2] == '10211'

def get_organisation_by_id_side_effect(organisation_id):
    if organisation_id == 1:
        return (1, None, '10211', 'CO', 'Cabinet Office', 'PURCHASE_ORDER', None, datetime.datetime(2023, 11, 8, 14, 41, 28), datetime.datetime(2025, 11, 4, 12, 51, 55))
    
    if organisation_id == 244:
        return (244, 1, '30440', 'CO-SUB', 'CO-SUB', 'PURCHASE_ORDER', None, datetime.datetime(2023, 11, 8, 14, 41, 28), datetime.datetime(2025, 12, 3, 11, 55, 43))
