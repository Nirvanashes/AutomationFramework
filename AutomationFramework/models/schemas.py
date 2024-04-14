from datetime import datetime

from pydantic import BaseModel


class UserBase(BaseModel):
    user_name: str


class LoginModel(UserBase):
    password: str


class CreateUser(LoginModel):
    user_email: str
    user_phone: int
    name: str


class UserInfo(UserBase):
    id: int
    user_email: str
    user_phone: int
    name: str
    create_time: datetime
    update_time: datetime
    is_active: int | None = None
    default_project_id: int | None = None

    class Config:
        # orm_mode = True
        from_attributes = True


class TokenModel(UserInfo):
    access_token: str
    token_type: str


class ProjectBase(BaseModel):
    project_id: int | None = None
    project_name: str
    parent_project_id: int | None = None
