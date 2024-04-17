from AutomationFramework.common.db.models import models
from AutomationFramework.dependencies import db_session
from AutomationFramework.schemas import interface_schemas


def query_interface(data: interface_schemas.QueryInterface):
    """
    获取未删除接口列表
    :param data:
    :return:
    """
    context_aware_session = db_session.get()
    context_aware_session.query()

    query = context_aware_session.query(models.InterfacePath).filter(models.InterfacePath.is_deleted == False)
    if data.interface_name is not None:
        query = query.filter(models.InterfacePath.interface_name.like(f"%{data.interface_name}%"))
    if data.url is not None:
        query = query.filter(models.InterfacePath.url == data.url)
    result = query.all()
    return result


def get_interface_by_id(interface_id):
    """
    根据id获取接口数据
    :param interface_id:
    :return:
    """
    context_aware_session = db_session.get()
    data = (context_aware_session.query(models.InterfacePath)
            .filter(models.InterfacePath.id == interface_id)
            .filter(models.InterfacePath.is_deleted == 0)
            .first())
    return data


def add_interface(interface: interface_schemas.CreateInterface, current_user):
    context_aware_session = db_session.get()
    data = models.InterfacePath(**interface.dict(), create_user=current_user.id, update_user=current_user.id)
    try:
        context_aware_session.add(data)
        context_aware_session.commit()
        context_aware_session.refresh(data)
        return data
    except Exception as e:
        context_aware_session.rollback()
        return e


def update_interface(interface: interface_schemas.UpdateInterface, current_user):
    context_aware_session = db_session.get()
    data = interface.dict()
    data['update_user'] = current_user.id
    (context_aware_session.query(models.InterfacePath)
     .filter(models.InterfacePath.id == interface.id)
     .filter(models.InterfacePath.is_deleted == 0)
     .update(data))
    try:
        context_aware_session.commit()
        return data
    except Exception as e:
        context_aware_session.rollback()
        return e


def delete_interface(interface_id, current_user):
    context_aware_session = db_session.get()
    data = (context_aware_session.query(models.InterfacePath)
            .filter(models.InterfacePath.id == interface_id)
            .filter(models.InterfacePath.is_deleted == 0)
            .first())
    data.is_deleted = 1
    data.update_user = current_user.id
    try:
        context_aware_session.commit()
        context_aware_session.refresh(data)
        return True
    except Exception as e:
        context_aware_session.rollback()
        return e
