from typing import Annotated

from fastapi import Depends
from sqlalchemy import or_, and_

from AutomationFramework.common.db.models import models
from AutomationFramework.dependencies import db_session
from AutomationFramework.models.project import generate_project_tree
from AutomationFramework.schemas import project_schemas, user_schemas
from AutomationFramework.utils.logger import Log

log = Log("base")


def query_projects():
    """
    获取未删除的项目树
    :return:
    """
    context_aware_session = db_session.get()
    data = (context_aware_session.query(models.Project)
            .filter(models.Project.is_deleted == 0)
            .all())
    tree = generate_project_tree(data)
    return tree


def query_project_by_id(project_id: int):
    context_aware_session = db_session.get()
    data = context_aware_session.query(models.Project).filter(
        models.Project.id == project_id and models.Project.is_deleted == 1).first()
    return data


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
    data = project.dict()
    data['update_user'] = current_user.id
    try:
        result = context_aware_session.query(models.Project).filter(models.Project.id == project.id).filter(
            models.Project.is_deleted == 1).update(data)
        context_aware_session.commit()
        return True
    except Exception as e:
        context_aware_session.rollback()
        log.error(e)
        return False



