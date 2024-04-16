from fastapi import APIRouter, Depends
from fastapi_pagination import Page, paginate
# from fastapi_pagination.ext.sqlalchemy import paginate
from typing import Annotated
from sqlalchemy.orm import Session
from AutomationFramework.dependencies import get_db_session, db_session
from AutomationFramework.common.db.crud import base_crud, user_crud
from AutomationFramework.schemas import user_schemas, project_schemas
from AutomationFramework.utils.logger import Log
from AutomationFramework.utils.user_token import get_current_active_user

router = APIRouter(
    prefix="/base",
    tags=["base"]
)
log = Log("base")


@router.get("/queryprojects.do", response_model=Page[project_schemas.ProjectList])
def query_projects(db: Session = Depends(get_db_session)):
    """
    获取未删除的项目列表
    :param db:
    :return:
    """
    db_session.set(db)
    data = base_crud.query_projects()
    return paginate(data)


@router.post("/addproject.do")
def add_project(project: project_schemas.ProjectBase,
                current_user: Annotated[user_schemas.UserInfo, Depends(get_current_active_user)],
                db: Session = Depends(get_db_session)):
    """
    添加项目或子项目
    :param project:
    :param current_user:
    :param db:
    :return:
    """
    db_session.set(db)
    return base_crud.add_project(project, current_user)


@router.post("/updateproject.do")
def update_project(project: project_schemas.UpdateProject,
                   current_user: Annotated[user_schemas.UserInfo, Depends(get_current_active_user)],
                   db: Session = Depends(get_db_session)):
    """
    更新项目
    :param project:
    :param current_user:
    :param db:
    :return:
    """
    db_session.set(db)
    return base_crud.update_or_delete_project(project, current_user)


@router.post("/deleteproject.do")
def delete_project(project: project_schemas.UpdateProject,
                   current_user: Annotated[user_schemas.UserInfo, Depends(get_current_active_user)],
                   db: Session = Depends(get_db_session)):
    """
    逻辑删除项目，is_deleted传入0即表示未删除
    :param project:
    :param current_user:
    :param db:
    :return:
    """
    db_session.set(db)
    return base_crud.update_or_delete_project(project, current_user)


@router.post("/updateuserproject.do")
def update_user_project(default_project:int,
                        current_user: Annotated[user_schemas.UserInfo, Depends(get_current_active_user)],
                        db: Session = Depends(get_db_session)):
    db_session.set(db)
    data = user_crud.update_user_project(default_project, current_user)
    return data


