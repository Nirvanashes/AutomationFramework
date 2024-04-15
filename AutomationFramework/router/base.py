from fastapi import APIRouter, HTTPException, Depends
from fastapi_pagination import Page, Params, add_pagination
from fastapi_pagination.ext.sqlalchemy import paginate
from typing import Annotated
from sqlalchemy.orm import Session
from AutomationFramework.depedencies import get_db_session, db_session
from AutomationFramework.common.sql import database, crud, models, base_crud
from AutomationFramework.models import user_schemas, project_schemas
from AutomationFramework.utils.logger import Log
from AutomationFramework.utils.userToken import get_current_active_user

router = APIRouter(
    prefix="/base",
    tags=["base"]
)
log = Log("base")


@router.get("queryprojects.do", response_model=Page[project_schemas.ProjectList])
def query_projects(db: Session = Depends(get_db_session)):
    pass


@router.post("/addproject.do")
def add_project(project: project_schemas.ProjectBase,
                current_user: Annotated[user_schemas.UserInfo, Depends(get_current_active_user)],
                db: Session = Depends(get_db_session)):
    db_session.set(db)
    return base_crud.add_project(project, current_user)


@router.post("/updateproject.do")
def update_project(project: project_schemas.UpdateProject,
                   current_user: Annotated[user_schemas.UserInfo, Depends(get_current_active_user)],
                   db: Session = Depends(get_db_session)):
    db_session.set(db)
    return base_crud.update_or_delete_project(project, current_user)


@router.post("/deleteproject.do")
def delete_project(project: project_schemas.UpdateProject,
                   current_user: Annotated[user_schemas.UserInfo, Depends(get_current_active_user)],
                   db: Session = Depends(get_db_session)):
    db_session.set(db)
    return base_crud.update_or_delete_project(project, current_user)


@router.post("/updateuserproject.do")
def update_user_project(user: user_schemas.UserBase, db: Session = Depends(get_db_session)):
    data = crud.update_user_project(user, db)
    return data


@router.post("/getprojectlist.do", response_model=Page[user_schemas.ProjectBase])
def get_child_project(project: user_schemas.ProjectBase, db: Session = Depends(get_db_session),
                      params: Params = Depends()):
    pass


add_pagination(router)
