# 服务器&数据库相关
from datetime import datetime
from pydantic import BaseModel


class ServerBase(BaseModel):
    name: str
    ip: str
    port: int
    account: str
    password: str
    type: int
    database_name: str | None = None
    description: str | None = None


class UpdateServer(ServerBase):
    id:int
    is_deleted: int = 0


class ServerInfo(ServerBase):
    id: int
    is_deleted: int = 0
    create_user: int
    create_date: datetime | None = None
    update_user: int
    update_date: datetime | None = None

    class Config:
        orm_mode = True
