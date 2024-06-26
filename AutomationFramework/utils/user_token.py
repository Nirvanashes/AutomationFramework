from datetime import timedelta, datetime
from typing import Optional, Annotated
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from fastapi import Depends, HTTPException,status
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from AutomationFramework.common.db.crud import user_crud
from AutomationFramework.dependencies import get_db_session, db_session
from AutomationFramework.schemas import user_schemas
from AutomationFramework.utils.symmetric_encryption import SymmetricEncryption
from AutomationFramework.config.config import settings


# 使用 "bcrypt" 算法对密码进行哈希
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login.do")
encryption = SymmetricEncryption()


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


def authenticate_user(username,password):
    """
    校验用户是否存在
    :param username:用户名
    :param password:未加密的密码
    :param db:
    :return:
    """
    data = user_crud.get_user_by_user_name(username)
    # todo：给密码加上对称加密，解密后再与数据库密码对比，前后端禁止密码明文传输
    decrypt_password = encryption.decrypt(password)
    if not data:
        return False
    if not verify_password(password, data.password):
        return False
    if not verify_password(decrypt_password, data.password):
        return False
    return data


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)],db: Session = Depends(get_db_session)):
    db_session.set(db)
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
        token_data = user_schemas.UserBase(user_name=username)
    except JWTError:
        raise credentials_exception
    user = user_crud.get_user_by_user_name(token_data.user_name)
    if user is None:
        raise credentials_exception
    return user


def get_current_active_user(current_user: Annotated[user_schemas.UserInfo, Depends(get_current_user)]):
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user
