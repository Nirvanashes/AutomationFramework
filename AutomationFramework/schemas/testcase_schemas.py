# 接口用例相关
from datetime import datetime
from pydantic import BaseModel


class TestCaseInfoBase(BaseModel):
    name: str
    interface_id: int
    status: int
    belong_project: int
    description: str | None = None


class QueryTestCase(BaseModel):
    name: str | None = None
    status: int | None = None
    belong_project: int | None = None


class CreateTestCase(TestCaseInfoBase):
    headers: dict | None = None
    parameters: dict
    expected_result: str
    server_path: int
    related_case: int | None = None


class UpdateTestCase(CreateTestCase):
    id: int
    is_deleted: int


class TestCaseInfo(TestCaseInfoBase):
    create_user: int
    update_user: int
    create_time: datetime
    update_time: datetime

    class Config:
        orm_mode = True


class TestCaseExecutionReport(BaseModel):
    id: int
    name: str
    total_num: int
    success_num: int
    fail_num: int
    skip_num: int
    belong_project: int
    create_user: int
    update_user: int
    create_time: datetime
    update_time: datetime
    is_deleted: int


class TestCaseExecutionRecord(BaseModel):
    testcase_id: int
    result_id: int
    status: int
    actual_results: str
    create_user: int
    update_user: int
    create_time: datetime
    update_time: datetime
    is_deleted: int
