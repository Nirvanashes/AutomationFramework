from AutomationFramework.common.db.models import models
from AutomationFramework.dependencies import db_session
from AutomationFramework.schemas import testcase_schemas


def query_test_cases(query: testcase_schemas.QueryTestCase):
    context_aware_session = db_session.get()
    data = context_aware_session.query(models.TestCaseInfo)
    if query.name is not None:
        data = data.filter(models.TestCaseInfo.name.like(f'%{query.name}%'))
    if query.status is not None:
        data = data.filter(models.TestCaseInfo.status == query.status)
    if query.belong_project is not None:
        data = data.filter(models.InterfacePath.belong_project == query.belong_project)
    result = data.all()
    return result


def add_test_case(request: testcase_schemas.CreateTestCase, current_user):
    context_aware_session = db_session.get()
    data = request.dict()
    data['create_user'] = current_user.id
    data['update_user'] = current_user.id
    try:
        context_aware_session.add(data)
        context_aware_session.commit()
        return True
    except Exception as e:
        context_aware_session.rollback()
        return e


def update_test_case(request: testcase_schemas.UpdateTestCase, current_user):
    context_aware_session = db_session.get()
    data = request.dict()
    data['update_user'] = current_user.id
    try:
        context_aware_session.query(models.TestCaseInfo).filter_by(id=request.id, is_deleted=0).update(data)
        context_aware_session.commit()
        return True
    except Exception as e:
        context_aware_session.rollback()
        return e


def delete_test_case(testcase_id:int, current_user):
    context_aware_session = db_session.get()
    try:
        (context_aware_session.query(models.TestCaseInfo)
         .filter_by(id=testcase_id, is_deleted=0)
         .update({models.TestCaseInfo.is_deleted:1,models.TestCaseInfo.update_user:current_user.id}))
        context_aware_session.commit()
        return True
    except Exception as e:
        context_aware_session.rollback()
        return e
