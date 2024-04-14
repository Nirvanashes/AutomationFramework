from datetime import datetime
from .database import Base, engine
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, func, TIMESTAMP, Index
from sqlalchemy.orm import relationship,mapped_column


# 基础信息表
class User(Base):
    """
    用户表
    """
    __tablename__ = "User"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, unique=True, doc="用户id")
    user_name = Column(String(100), unique=True, doc="用户名")
    name = Column(String(100), doc="姓名")
    password = Column(String(100), doc="密码")
    user_email = Column(String(100), unique=True, doc="用户邮箱")
    user_phone = Column(Integer, unique=True, doc="手机号")
    user_type = Column(Integer,default=0, doc="用户类型：0:普通用户，1:管理员")
    create_time = Column(DateTime,default=datetime.now, doc="创建时间")
    update_time = Column(DateTime,default=datetime.now, onupdate=datetime.now, doc="更新时间")
    # last_login = Column(TIMESTAMP, doc="上次登录时间")
    default_project = Column(String,default=None, doc="默认项目", comment="默认项目")
    is_active = Column(Integer, default=1, doc="用户是否启用,0:禁用‘1:启用")


class Project(Base):
    """
    项目表
    """
    __tablename__ = "Project"
    id = Column(Integer, primary_key=True, autoincrement=True)
    project_name = Column(String)
    parent_project_id = Column(Integer)
    create_time = Column(DateTime, default=datetime.now, doc="创建时间")
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now, doc="更新时间")
    is_deleted = Column(Integer, default=0,doc="是否删除")


class Server(Base):
    """
    服务器配置表

    """
    __tablename__ = "Server"
    id = Column(Integer, primary_key=True, autoincrement=True)
    server_name = Column(String,doc="服务器名称")
    server_ip = Column(String,doc="服务器ip")
    server_port = Column(Integer,doc="服务器端口")
    server_user = Column(String,doc="服务器账号")
    server_password = Column(String,doc="服务器密码")
    server_type = Column(Integer,doc="服务器类型：0:服务器，1:数据库")
    create_time = Column(DateTime,doc="创建时间")
    create_user = Column(Integer,doc="创建人id")
    update_time = Column(DateTime,doc="更新时间")
    update_user = Column(Integer,doc="更新人id")
    is_deleted = Column(Integer, default=0)


# 接口测试相关表
class InterfacePath(Base):
    """
    接口信息表
    """
    __tablename__ = "InterfacePath"
    id = Column(Integer, primary_key=True, autoincrement=True)
    interface_name = Column(String, doc="接口名称")
    interface_path = Column(String, doc="接口地址")
    interface_type = Column(Integer,doc="接口请求方式：0:get，1:post，2:")
    protocol = Column(Integer, doc="协议：0:http，1:https协议", comment="协议：0:http，1:https协议")
    description = Column(String, doc="接口描述")
    ip_port = Column(String, doc="接口服务器地址")
    source = Column(String, doc="来源：0:手工录入；1:yapi同步；")
    create_time = Column(DateTime)
    create_user = Column(Integer,doc="创建人id")
    update_time = Column(DateTime)
    update_user = Column(Integer,doc="更新人id")
    is_deleted = Column(Integer, default=0)



# 性能测试相关表
class LoadResource(Base):
    """施压机资源."""
    # def __init__(self):
    #     pass
    __tablename__ = 'load_resource'  # 数据库名字
    id = Column(Integer, primary_key=True, doc='主键', comment='主键')  # 压测资源主键，comment为列注释
    resource_ip = Column(String(50), doc='资源ip', comment='资源ip')  # 压测资源IP
    resource_zone = Column(String(50), doc='资源区域', comment='资源区域')  # 压测资源区域
    project_id = Column(String(250), doc='项目id', comment='项目id')  # 占用资源的项目ID
    scene_id = Column(String(250), doc='场景id', comment='场景id')  # 占用资源的场景ID
    task_name = Column(String(250))  # 占用资源的任务名字
    task_uid = Column(String(250), doc='任务id', comment='任务id')  # 占用资源的任务ID，根据任务ID可以得知项目和场景信息
    resource_status = Column(Boolean, default=False, doc='资源状态', comment='资源状态')  # 压测资源可用状态,默认False表示可用
    gmt_create = Column(DateTime,default=datetime.now, doc='创建时间', comment='创建时间')  # 创建时间
    gmt_modify = Column(DateTime,default=datetime.now, onupdate=datetime.now, doc='更新时间',
                        comment='更新时间')  # 修改时间
    __table_args__ = (
        Index('index(zone,status)', 'resource_zone', 'resource_status'), {'comment': '压测资源表'})  # 添加索引和表注释
