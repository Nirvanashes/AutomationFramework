from datetime import datetime

from pydantic import BaseModel


# 接口相关
class InterfacePathBase(BaseModel):
    interface_name: str
    method: str
    headers: dict | None = None
    url: str
    parameters: dict | None = None
    type: int


class CreateInterface(InterfacePathBase):
    protocol: int | None
    description: str | None = None
    server_path: int
    source: int = 0
    belong_project: int | None = None


class UpdateInterface(CreateInterface):
    id: int


class InterfaceInfo(CreateInterface):
    id: int
    case_num:int
    status:int
    create_time: datetime
    create_user: int
    update_time: datetime
    update_user: int
    is_deleted: int

    class Config:
        from_attributes = True


class QueryInterface(BaseModel):
    interface_name: str | None = None
    url: str | None = None
