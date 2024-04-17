# 项目相关
from datetime import datetime

from pydantic import BaseModel


class ProjectBase(BaseModel):
    project_name: str | None = None
    parent_project_id: int | None = None


class UpdateProject(ProjectBase):
    id: int
    is_deleted: int = 0


class ProjectInfo(ProjectBase):
    id: int
    is_deleted: int
    update_user: int
    create_time: datetime
    update_time: datetime


class ProjectList(ProjectInfo):
    children: list[ProjectInfo] | None = None

    class Config:
        orm_mode = True
