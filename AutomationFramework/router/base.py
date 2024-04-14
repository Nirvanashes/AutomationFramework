from fastapi import APIRouter, HTTPException, Depends
from fastapi_pagination import Page, Params, add_pagination
from fastapi_pagination.ext.sqlalchemy import paginate
from typing import Annotated
from sqlalchemy.orm import Session
from AutomationFramework.depedencies import get_db_session
from AutomationFramework.common.sql import database, crud, models
from AutomationFramework.models import schemas
from AutomationFramework.utils.logger import Log

router = APIRouter(
    prefix="/base",
    tags=["base"]
)


@router.get("/getproject.do")
def get_project(user_id: int, db: Session = Depends(get_db_session)):
    log = Log("查询用户")
    log.info("查询用户看看")
    data = crud.get_user_by_user_id(user_id, db)
    return data


@router.post("/addproject.do")
def add_project(project: schemas.ProjectBase, db: Session = Depends(get_db_session)):
    data = crud.add_project(project, db)
    return data


@router.post("/updateuserproject.do")
def update_user_project(user: schemas.UserBase, db: Session = Depends(get_db_session)):
    data = crud.update_user_project(user, db)
    return data


@router.post("/getchildproject.do", response_model=Page[schemas.ProjectBase])
def get_child_project(project: schemas.ProjectBase, db: Session = Depends(get_db_session), params: Params = Depends()):
    pass


add_pagination(router)
