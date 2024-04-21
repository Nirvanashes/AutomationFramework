from datetime import timedelta
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

from fastapi_pagination import Page, paginate
from sqlalchemy.orm import Session
from AutomationFramework.dependencies import get_db_session, db_session
from AutomationFramework.common.db.crud import user_crud, testcase_crud
from AutomationFramework.models.testcase import executed_testcase
from AutomationFramework.schemas import user_schemas, testcase_schemas
from AutomationFramework.utils.logger import Log
from AutomationFramework.utils.user_token import authenticate_user, get_current_active_user, create_access_token, \
    get_password_hash
from AutomationFramework.config.config import settings

router = APIRouter(
    prefix="/testcase",
    tags=["testcase"]
)

log = Log("testcase")


@router.get("/queryTestCase.do", response_model=Page[testcase_schemas.TestCaseInfo])
# todo:修改参数
def query_testcase(
        query: testcase_schemas.QueryTestCase,
        db: Session = Depends(get_db_session)
):
    db_session.set(db)
    result = testcase_crud.query_test_cases(query)
    return paginate(result)


@router.post("/addTestcase.do")
def add_testcase(data: testcase_schemas.CreateTestCase,
                 current_user: Annotated[user_schemas.UserInfo, Depends(get_current_active_user)],
                 db: Session = Depends(get_db_session)):
    db_session.set(db)
    result = testcase_crud.add_test_case(data, current_user)
    return result


@router.post("updateTestcase.do")
def update_testcase(data: testcase_schemas.UpdateTestCase,
                    current_user: Annotated[user_schemas.UserInfo, Depends(get_current_active_user)],
                    db: Session = Depends(get_db_session)):
    db_session.set(db)
    result = testcase_crud.update_test_case(data, current_user)
    return result


@router.post("/deleteTestcase.do")
def delete_testcase(testcase_id: int,
                    current_user: Annotated[user_schemas.UserInfo, Depends(get_current_active_user)],
                    db: Session = Depends(get_db_session)):
    db_session.set(db)
    return testcase_crud.delete_test_case(testcase_id, current_user)


# 执行接口用例
@router.post("/executeInterfaceUseCases.do")
async def execute_interface_testcases(data: testcase_schemas.ExecuteInterfaceTestCases,
                                current_user: Annotated[user_schemas.UserInfo, Depends(get_current_active_user)],
                                db: Session = Depends(get_db_session)):
    db_session.set(db)
    result = await executed_testcase(data, current_user)
    return result
