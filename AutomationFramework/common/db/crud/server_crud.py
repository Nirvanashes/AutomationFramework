from sqlalchemy import and_

from AutomationFramework.common.db.models import models
from AutomationFramework.dependencies import db_session
from AutomationFramework.schemas import server_schemas


def query_server_list(name: str = None, ip: int = None):
    context_aware_session = db_session.get()
    query = context_aware_session.query(models.ServerInfo)
    if name is not None:
        query = query.filter(models.ServerInfo.name.like(f"%{name}%"))
    if ip is not None:
        query = query.filter(models.ServerInfo.ip == ip)
    result = query.all()
    return result


def get_serverinfo_by_id(server_id: int):
    context_aware_session = db_session.get()
    query = context_aware_session.query(models.ServerInfo).filter(models.ServerInfo.id == server_id).first()
    return query


def add_server(request: server_schemas.ServerBase, current_user):
    context_aware_session = db_session.get()
    data = models.ServerInfo(**request.dict(),
                             create_user=current_user.id,
                             update_user=current_user.id)
    try:
        context_aware_session.add(data)
        context_aware_session.commit()
        return True
    except Exception as e:
        context_aware_session.rollback()
        raise e


def update_server(request: server_schemas.UpdateServer, current_user):
    context_aware_session = db_session.get()
    data = request.dict(exclude_none=True)
    data['update_user'] = current_user.id
    try:
        result = ((context_aware_session.query(models.ServerInfo)
                   .filter(and_(models.ServerInfo.id == request.id, models.ServerInfo.is_deleted == 0)))
                  .update(data))
        context_aware_session.commit()
        context_aware_session.refresh(data)
        return True
    except Exception as e:
        raise e
