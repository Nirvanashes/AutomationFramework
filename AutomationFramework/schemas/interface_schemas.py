from datetime import datetime

from pydantic import BaseModel


# 接口相关
class InterfacePathBase(BaseModel):
    method: str
    headers: dict | None = None
    url: str
    parameters: dict | None = None
    type: str | None = None


class CreateInterface(InterfacePathBase):
    interface_name: str
    protocol: str | None
    description: str
    serverpath: str
    source: int
    belong_project: int | None = None


class InterfaceInfo(CreateInterface):
    id: int
    create_time: datetime
    create_user: int
    update_time: datetime
    update_user: int
    is_deleted: bool

    class Config:
        from_attributes = True


class QueryInterface(BaseModel):
    interface_name: str | None = None
    url: str | None = None
