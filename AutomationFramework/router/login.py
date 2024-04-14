from datetime import timedelta
from fastapi import APIRouter, HTTPException, Depends, status,Header
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from sqlalchemy.orm import Session
from AutomationFramework.depedencies import get_db_session
from AutomationFramework.common.sql import database, crud, models
from AutomationFramework.models import user_schemas
from AutomationFramework.utils.logger import Log
from AutomationFramework.utils.userToken import authenticate_user, get_current_active_user, create_access_token, \
    get_password_hash
from config import settings

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

log = Log("user")

@router.post("/signup.do", response_model=user_schemas.UserInfo)
def sign(*, data: user_schemas.CreateUser, db: Session = Depends(get_db_session)):
    """
    用户注册
    :param data:
    :param db:
    :return:
    """

    user = crud.get_user_by_user_name(data.user_name, db)
    if user is not None:
        log.error("用户已存在")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户已存在"
        )

    data.password = get_password_hash(data.password)
    result = crud.create_user(data, db)
    return result


@router.post("/login.do")
def login(*, form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
          db: Session = Depends(get_db_session)) -> user_schemas.TokenModel:
    """
    用户token登录接口
    :param form_data:
    :param db:
    :return:
    """
    user_info = authenticate_user(form_data.username, form_data.password, db)
    if not user_info:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password",
                            headers={"WWW-Authenticate": "Bearer"}
                            )
    access_token_expires = timedelta(minutes=settings.token['ACCESS_TOKEN_EXPIRE_MINUTES'])
    access_token = create_access_token(
        data={"sub": user_info.user_name},
        expires_delta=access_token_expires
    )
    user_info.access_token = access_token
    user_info.token_type = "bearer"
    return user_info


@router.get("/userinfo.do", response_model=user_schemas.UserInfo)
def get_user_info(current_user: Annotated[user_schemas.UserInfo, Depends(get_current_active_user)]):
    return current_user
