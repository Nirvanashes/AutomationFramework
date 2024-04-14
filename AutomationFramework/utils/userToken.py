from datetime import timedelta, datetime
from typing import Optional, Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from fastapi import Header, Depends, HTTPException,status
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from AutomationFramework.common.sql import crud
from AutomationFramework.depedencies import get_db_session
from AutomationFramework.models import schemas
from config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login.do")
db1 = get_db_session()


def get_password_hash(password: str) -> str:
    """
    对用户密码进行hash
    :param password:
    :return: hash后的password
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    校验用户输入的密码与hash后的密码是否相同
    :param plain_password:
    :param hashed_password:
    :return:返回校验结果
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    用户登录生成token
    :param data:
    :param expires_delta:
    :return:
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.token["SECRET_KEY"], algorithm=settings.token["ALGORITHM"])
    return encoded_jwt


def authenticate_user(username,password, db: Session):
    """
    校验用户是否存在
    :param username:
    :param password:
    :param db:
    :return:
    """
    data = crud.get_user_by_user_name(username, db)
    if not data:
        return False
    if not verify_password(password, data.password):
        return False
    return data


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)],db: Session = Depends(get_db_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, settings.token["SECRET_KEY"], algorithms=settings.token["ALGORITHM"])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.UserBase(user_name=username)
    except JWTError:
        raise credentials_exception
    user = crud.get_user_by_user_name(token_data.user_name, db)
    if user is None:
        raise credentials_exception
    return user


def get_current_active_user(current_user: Annotated[schemas.UserInfo, Depends(get_current_user)]):
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user
