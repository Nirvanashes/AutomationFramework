from typing import Annotated

from AutomationFramework.common.sql.database import SessionLocal
from fastapi import Header, HTTPException


def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
