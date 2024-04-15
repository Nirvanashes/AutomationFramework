import datetime
from AutomationFramework.depedencies import get_db_session, db_session
from AutomationFramework.utils.userToken import get_password_hash

from sqlalchemy.orm import Session
from AutomationFramework.models import user_schemas
from AutomationFramework.common.sql import database, models


def get_user_by_user_id(user_id: int):
    context_aware_session = db_session.get()
    return context_aware_session.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_user_name(username: str):
    context_aware_session = db_session.get()
    return context_aware_session.query(models.User).filter(models.User.user_name == username).filter(models.User.is_active == True).first()


def create_user(user: user_schemas.CreateUser):
    context_aware_session = db_session.get()
    try:
        user_data = models.User(**user.dict(),
                                user_type=0,
                                is_active=True)
        context_aware_session.add(user_data)
        context_aware_session.commit()
        context_aware_session.refresh(user_data)
        return user_data
    except Exception as e:
        context_aware_session.rollback()


def update_user_by_id(user: user_schemas.UserBase):
    context_aware_session = db_session.get()
    pass


def update_user_project(user: user_schemas.UserBase):
    context_aware_session = db_session.get()
    user_project = models.User(user_id=user.user_id, default_project=user.default_project)
    try:
        # context_aware_session.add(user_project)
        context_aware_session.commit()
        context_aware_session.refresh(user_project)
        return user_project
    except Exception as e:
        context_aware_session.rollback()


def query_project_by_id(project_id: int):
    context_aware_session = db_session.get()
    data = context_aware_session.query(models.Project).filter(models.Project.id == project_id and models.Project.is_deleted == 0).all()
    return data



