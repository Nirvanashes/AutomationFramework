# 接口用例相关
from datetime import datetime
from typing import Any

from pydantic import BaseModel


# 接口用例页
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


class TestCaseInfo(CreateTestCase):
    create_user: int
    update_user: int
    create_time: datetime
    update_time: datetime

    class Config:
        orm_mode = True


class ExecuteInterfaceTestCases(BaseModel):
    belong_project: int
    server_path: int
    testcase_type: int  # 0：全部用例，1:我创建的


class BuildInterfaceTestCases(BaseModel):
    url: str | bytes = None
    method: str | None = None
    params: dict | None = None
    data: dict | None = None
    headers: dict | None = None
    cookies: Any | None = None
    files: Any | None = None
    auth: Any | None = None
    timeout: Any | None = None
    allow_redirects: bool | None = None
    proxies: Any | None = None
    hooks: Any | None = None
    stream: bool | None = None
    verify: Any | None = None
    cert: Any | None = None
    json: Any | None = None


# class ConstructTheRequestBody(BaseModel):
#     url: str
#     method: str
#     headers: dict | None = None
#     url: str
#     parameters: dict | None = None


# 接口用例报告页相关
class TestCaseExecutionReportBase(BaseModel):
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


class TestCaseExecutionReport(TestCaseExecutionReportBase):
    pass


class CreateTestCaseExecutionReport(BaseModel):
    name = str
    total_num: int


class UpdateTestCaseExecutionReport(CreateTestCase):
    id: int
    success_num: int
    fail_num: int
    skip_num: int
    update_user: int



# 接口执行情况详情
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
