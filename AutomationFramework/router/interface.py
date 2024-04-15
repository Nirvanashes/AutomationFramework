from datetime import timedelta
from fastapi import APIRouter, HTTPException, Depends, status, Header
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from sqlalchemy.orm import Session
from AutomationFramework.depedencies import get_db_session, db_session
from AutomationFramework.common.sql import database, models, interface_crud
from AutomationFramework.models import user_schemas, interface_schemas
from AutomationFramework.utils.logger import Log
from AutomationFramework.utils.userToken import authenticate_user, get_current_active_user, create_access_token, \
    get_password_hash
from config import settings
from AutomationFramework.middleware.HttpClint import Request

router = APIRouter(
    prefix="/interface",
    tags=["interface"]
)
log = Log("interface")


@router.post("/httprequest.do")
def http_request(request: interface_schemas.InterfacePathBase):
    if not request.method:
        log.error("请求方式不能为空！")
        return {"code": status.HTTP_400_BAD_REQUEST, "message": "请求方式不能为空"}
    if not request.url:
        log.error("请求地址不能为空！")
        return {"code": status.HTTP_400_BAD_REQUEST, "message": "请求地址不能为空"}
    r = Request(url=request.url, data=request.data, headers=request.headers)
    response = r.request(request.method)
    return response


@router.post("/addinterface.do")
def add_interface(request: interface_schemas.CreateInterface, db: Session = Depends(get_db_session)):
    db_session.set(db)
    data = interface_crud.add_interface(request)


@router.post("/getinterface.do")
def get_interface(interface_id: int, db: Session = Depends(get_db_session)):
    db_session.set(db)
    data = interface_crud.get_interface_by_id(interface_id)
    return data


@router.post("/queryinterface.do")
def query_interface(query: interface_schemas.queryInterface, db: Session = Depends(get_db_session)):
    db_session.set(db)
    data = interface_crud.query_interface(query)
    return data
