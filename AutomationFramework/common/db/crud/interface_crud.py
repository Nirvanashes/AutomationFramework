from AutomationFramework.common.db.models import models
from AutomationFramework.dependencies import db_session
from AutomationFramework.schemas import interface_schemas


def get_all_interfaces():
    """
    获取全部接口
    :return:
    """
    context_aware_session = db_session.get()
    return context_aware_session.query(models.InterfacePath).filter(models.InterfacePath.is_deleted == 0).all()


def query_interface(querydata: interface_schemas.QueryInterface):
    """
    查询接口
    :param querydata:
    :return:
    """
    context_aware_session = db_session.get()
    context_aware_session.query()
    return context_aware_session.query(models.InterfacePath).filter().all()


def get_interface_by_id(interface_id):
    """
    根据id获取接口数据
    :param interface_id:
    :return:
    """
    context_aware_session = db_session.get()
    return context_aware_session.query(models.InterfacePath).filter(models.InterfacePath.id == interface_id).first()


def get_interface_by_name(interface_name):
    context_aware_session = db_session.get()
    return context_aware_session.query(models.InterfacePath).filter(models.InterfacePath.name == interface_name).all()


def add_interface(interface: interface_schemas.CreateInterface):
    context_aware_session = db_session.get()
    data = models.InterfacePath(**interface.dict())
    try:
        context_aware_session.add(data)
        context_aware_session.commit()
        context_aware_session.refresh(data)
        return data
    except Exception as e:
        context_aware_session.rollback()


def update_interface(interface: interface_schemas.CreateInterface):
    pass


def delete_interface(interface_id):
    context_aware_session = db_session.get()
    data = context_aware_session.query(models.InterfacePath).filter(models.InterfacePath.id == interface_id).filter(
        models.InterfacePath.is_deleted == 0).first()
    data["is_deleted"] = 1
    try:
        context_aware_session.commit()
        context_aware_session.refresh(data)
        return data
    except Exception as e:
        context_aware_session.rollback()
