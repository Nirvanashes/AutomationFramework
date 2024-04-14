import datetime
from AutomationFramework.depedencies import get_db_session
from AutomationFramework.utils.userToken import get_password_hash

from sqlalchemy.orm import Session
from AutomationFramework.models import user_schemas
from AutomationFramework.common.sql import database, models


def get_user_by_user_id(user_id: int, db: Session):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_user_name(username: str, db: Session):
    return db.query(models.User).filter(models.User.user_name == username).filter(models.User.is_active == True).first()


def create_user(user: user_schemas.CreateUser, db: Session):
    try:
        user_data = models.User(**user.dict(),
                                user_type=0,
                                is_active=True)
        db.add(user_data)
        db.commit()
        db.refresh(user_data)
        return user_data
    except Exception as e:
        db.rollback()


def update_user_by_id(db: Session, user: user_schemas.UserBase):
    pass


def update_user_project(user: user_schemas.UserBase, db: Session):
    user_project = models.User(user_id=user.user_id, default_project=user.default_project)
    db.add(user_project)
    db.commit()
    db.refresh(user_project)
    return user_project


def query_project_by_id(project_id: int, db: Session):
    data = db.query(models.Project).filter(models.Project.id == project_id and models.Project.is_deleted == 0).all()
    return data


def add_project(project: user_schemas.ProjectBase, db: Session):
    data = models.Project(project_name=project.project_name, parent_project_id=project.parent_project_id)
    db.add(data)
    db.commit()
    db.refresh(data)
    return data


def delete_project_by_id(project: user_schemas.ProjectBase, db: Session):
    pass
