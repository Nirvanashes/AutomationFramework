# 项目相关
from pydantic import BaseModel


class ProjectBase(BaseModel):
    project_id: int | None = None
    project_name: str
    parent_project_id: int | None = None
