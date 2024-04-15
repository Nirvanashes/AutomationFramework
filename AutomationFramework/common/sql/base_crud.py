from typing import Annotated

from fastapi import Depends

from AutomationFramework.common.sql import models
from AutomationFramework.depedencies import db_session
from AutomationFramework.models import project_schemas, user_schemas
from AutomationFramework.utils.logger import Log
from AutomationFramework.utils.userToken import get_current_active_user

log = Log("base")


def get_all_projects():
    """
    返回所有未删除的项目列表
    :return:
    """
    context_aware_session = db_session.get()


def add_project(project: project_schemas.ProjectBase, current_user):
    context_aware_session = db_session.get()

    data = models.Project(**project.dict(),
                          create_user=current_user.id,
                          update_user=current_user.id)
    try:
        context_aware_session.add(data)
        context_aware_session.commit()
        context_aware_session.refresh(data)
        return data
    except Exception as e:
        context_aware_session.rollback()


def update_or_delete_project(project: project_schemas.UpdateProject, current_user):
    """
    用于更新项目或逻辑删除项目
    :param project:
    :param current_user:
    :return:
    """
    context_aware_session = db_session.get()
    # data = project.dict()['update_user'] = current_user.id
    try:
        # data = context_aware_session.query(models.Project).filter(models.Project.id == project.id).filter(models.Project.is_deleted == 1).update(project.dict())
        (context_aware_session.query(models.Project)
         .filter_by(id=project.id, is_deleted=1)
         .update(models.Project(**project.dict(),update_user=current_user.id)))
        context_aware_session.commit()
        return True
    except Exception as e:
        context_aware_session.rollback()
        log.error(e)
        return False
