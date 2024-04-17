from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi_pagination import Page, paginate
from sqlalchemy.orm import Session
from AutomationFramework.dependencies import get_db_session, db_session
from AutomationFramework.common.db.crud import interface_crud
from AutomationFramework.schemas import interface_schemas, user_schemas
from AutomationFramework.utils.logger import Log
from AutomationFramework.middleware.http_client import Request
from AutomationFramework.utils.user_token import get_current_active_user

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


@router.post("/addInterface.do")
def add_interface(request: interface_schemas.CreateInterface,
                  current_user: Annotated[user_schemas.UserInfo, Depends(get_current_active_user)],
                  db: Session = Depends(get_db_session)):
    """
    添加接口
    :param current_user:
    :param request:
    :param db:
    :return:
    """
    db_session.set(db)
    data = interface_crud.add_interface(request, current_user)
    return data


@router.post("/getInterfaceInfo.do")
def get_interface(interface_id: int, db: Session = Depends(get_db_session)):
    """
    获取接口详情
    :param interface_id:
    :param db:
    :return:
    """
    db_session.set(db)
    data = interface_crud.get_interface_by_id(interface_id)
    return data


@router.post("/queryInterface.do", response_model=Page[interface_schemas.InterfaceInfo])
# todo：修改参数
def query_interface(query: interface_schemas.QueryInterface,
                    db: Session = Depends(get_db_session)):
    """
    获取接口列表，根据接口名称和接口地址查询
    :param query:
    :param db:
    :return:
    """
    db_session.set(db)
    data = interface_crud.query_interface(query)
    return paginate(data)


@router.post("/updateInterface.do")
def update_interface(data: interface_schemas.UpdateInterface,
                     current_user: Annotated[user_schemas.UserInfo, Depends(get_current_active_user)],
                     db: Session = Depends(get_db_session)):
    """
    更新接口
    :param data:
    :param current_user:
    :param db:
    :return:
    """
    db_session.set(db)
    data = interface_crud.update_interface(data, current_user)
    return data


@router.post("deleteInterface.do")
def delete_interface(interface_id: int,
                     current_user: Annotated[user_schemas.UserInfo, Depends(get_current_active_user)],
                     db: Session = Depends(get_db_session)):
    """
    逻辑删除接口
    :param interface_id:
    :param current_user:
    :param db:
    :return:
    """
    db_session.set(db)
    data = interface_crud.delete_interface(interface_id, current_user)
    return data
