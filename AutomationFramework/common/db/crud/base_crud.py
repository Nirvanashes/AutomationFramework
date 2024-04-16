from typing import Annotated

from fastapi import Depends
from sqlalchemy import or_, and_

from AutomationFramework.common.db.models import models
from AutomationFramework.dependencies import db_session
from AutomationFramework.schemas import project_schemas, user_schemas
from AutomationFramework.utils.logger import Log

log = Log("base")


def generate_project_tree(projects, parent_id=None):
    """
    :param projects:
    :param parent_id:
    :return:
    """
    tree = []
    for project in projects:
        if project.parent_project_id == parent_id:
            formatted_project = {
                "project_name": project.project_name,
                "parent_project_id": project.parent_project_id,
                "id": project.id,
                "is_deleted": project.is_deleted,
                "update_user": project.update_user,
                "create_time": project.create_time,
                "update_time": project.update_time,
                "children": generate_project_tree(projects, project.id)
            }
            tree.append(formatted_project)
    return tree


def query_projects():
    """

    :return:
    """
    context_aware_session = db_session.get()
    data = (context_aware_session.query(models.Project)
            .filter(models.Project.is_deleted == 1)
            .all())
    tree = generate_project_tree(data)
    return tree


def query_project_by_id(project_id: int):
    context_aware_session = db_session.get()
    data = context_aware_session.query(models.Project).filter(
        models.Project.id == project_id and models.Project.is_deleted == 1).all()
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
