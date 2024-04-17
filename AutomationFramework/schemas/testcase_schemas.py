# 接口用例相关
from datetime import datetime
from pydantic import BaseModel


class TestCaseBase(BaseModel):
    pass


class TestCaseExecutionReport(BaseModel):
    pass


class TestCaseExecutionRecord(BaseModel):
    pass
