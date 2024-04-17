from datetime import timedelta
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from sqlalchemy.orm import Session
from AutomationFramework.dependencies import get_db_session, db_session
from AutomationFramework.common.db.crud import user_crud
from AutomationFramework.schemas import user_schemas
from AutomationFramework.utils.logger import Log
from AutomationFramework.utils.user_token import authenticate_user, get_current_active_user, create_access_token, \
    get_password_hash
from AutomationFramework.config.config import settings

router = APIRouter(
    prefix="/testcase",
    tags=["testcase"]
)

log = Log("testcase")