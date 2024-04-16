import datetime
from AutomationFramework.dependencies import get_db_session, db_session
from AutomationFramework.utils.user_token import get_password_hash

from sqlalchemy.orm import Session
from AutomationFramework.schemas import user_schemas
from AutomationFramework.common.db.models import models
from AutomationFramework.common.db import database


def get_user_by_user_id(user_id: int):
    context_aware_session = db_session.get()
    return context_aware_session.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_user_name(username: str):
    context_aware_session = db_session.get()
    return context_aware_session.query(models.User).filter(models.User.user_name == username).filter(
        models.User.is_active == True).first()


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


def update_user_project(default_project, current_user):
    context_aware_session = db_session.get()
    (context_aware_session.query(models.User)
     .filter_by(id=current_user.id)
     .update({models.User.default_project: default_project}))
    try:
        context_aware_session.commit()
        return True
    except Exception as e:
        context_aware_session.rollback()
