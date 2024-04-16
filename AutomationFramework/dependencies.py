from contextvars import ContextVar
from typing import Annotated

from sqlalchemy.orm import Session

from AutomationFramework.common.db.database import SessionLocal
from fastapi import Header, HTTPException


def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# seesion上下文管理器，使用db_session.set(db)、db_session.get(db)获取session
db_session: ContextVar[Session] = ContextVar('db_session')
