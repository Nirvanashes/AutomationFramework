from datetime import datetime
from .database import Base, engine
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, func, TIMESTAMP, Index


# from sqlalchemy.orm import relationship,mapped_column


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
    user_type = Column(Integer, default=0, doc="用户类型：0:普通用户，1:管理员")
    create_time = Column(DateTime, default=datetime.now, doc="创建时间")
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now, doc="更新时间")
    default_project = Column(String, default=None, doc="默认项目", comment="默认项目")
    is_active = Column(Integer, default=1, doc="用户是否启用,0:禁用‘1:启用")
    __table_args__ = ({'comment': '用户表'})


class Project(Base):
    """
    项目表
    """
    __tablename__ = "Project"
    id = Column(Integer, primary_key=True, autoincrement=True)
    project_name = Column(String)
    parent_project_id = Column(Integer)
    create_user = Column(Integer, comment="创建人id")
    update_user = Column(Integer, comment="更新人id")
    create_time = Column(DateTime, default=datetime.now, doc="创建时间")
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now, doc="更新时间")
    is_deleted = Column(Integer, default=1, comment="是否删除，默认未删除")
    __table_args__ = ({'comment': '项目表'})


class ServerInfo(Base):
    """
    服务器&数据库配置表
    """
    __tablename__ = "Server"
    id = Column(Integer, primary_key=True, autoincrement=True)
    server_name = Column(String, doc="服务器名称")
    server_ip = Column(String, doc="服务器ip")
    server_port = Column(Integer, doc="服务器端口")
    server_user = Column(String, doc="服务器账号")
    server_password = Column(String, doc="服务器密码")
    server_type = Column(Integer, doc="服务器类型：0:服务器，1:数据库")
    database_name = Column(Integer, comment="数据库表")
    create_user = Column(Integer, doc="创建人id")
    update_user = Column(Integer, doc="更新人id")
    create_time = Column(DateTime, default=datetime.now, doc="创建时间")
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now, doc="更新时间")
    is_deleted = Column(Integer, default=1, comment="是否删除，默认未删除")
    __table_args__ = ({'comment': '服务器&数据库配置表'})


class InterfacePath(Base):
    """
    接口信息表
    """
    __tablename__ = "InterfacePath"
    id = Column(Integer, primary_key=True, autoincrement=True)
    interface_name = Column(String, comment="接口名称")
    protocol = Column(Integer, comment="协议：0:http，1:https协议")
    method = Column(String, comment="接口请求方式:get，post")
    headers = Column(String, comment="接口headers信息")
    url = Column(String, comment="接口地址")
    type = Column(String, comment="请求体类型：1:query，2:form-data，3:json")
    parameters = Column(String, comment="请求参数样例")
    description = Column(String, comment="接口描述")
    server_path = Column(String, comment="接口服务器地址")
    status = Column(Integer, comment="是否有效，默认有效", default=0)
    source = Column(Integer, comment="来源：0:手工录入；1:yapi同步；")
    belong_project = Column(Integer, comment="所属项目id", default=None)
    case_num = Column(Integer, comment="接口关联用例数量？")
    create_user = Column(Integer, comment="创建人id")
    update_user = Column(Integer, comment="更新人id")
    create_time = Column(DateTime, default=datetime.now, comment="创建时间")
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")
    is_deleted = Column(Integer, default=1, comment="是否删除，默认未删除")
    __table_args__ = ({'comment': '接口信息表'})


class TestCaseInfo(Base):
    """
    接口用例表
    """
    __tablename__ = "testcase_info"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, comment="接口用例名称")
    interface_id = Column(Integer, comment="对应接口id")
    parameters = Column(String, comment="用例参数")
    status = Column(Integer, default=1, comment="用例启用状态，0:未启用,1:启用")
    expected_result = Column(String, comment="预期结果")
    description = Column(String, comment="描述")
    server_path = Column(String, comment="接口用例执行对应的服务器地址")
    belong_project = Column(Integer, comment="所属项目")
    related_case = Column(Integer, comment="关联测试用例，优先执行关联用例")
    create_user = Column(Integer, comment="创建人id")
    update_user = Column(Integer, comment="更新人id")
    create_time = Column(DateTime, default=datetime.now, comment="创建时间")
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")
    is_deleted = Column(Integer, default=1, comment="是否删除，默认未删除")
    __table_args__ = ({'comment': '接口用例信息表'})


class TestCaseExecution(Base):
    """
    用例执行记录主表
    """
    __tablename__ = "testcase_execution"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, comment="执行名称")
    total_num = Column(Integer, comment="用例总数")
    success_num = Column(Integer, comment="执行成功数")
    fail_num = Column(Integer, comment="执行失败数")
    skip_num = Column(Integer, comment="跳过用例数")
    create_user = Column(Integer, comment="创建人id")
    update_user = Column(Integer, comment="更新人id")
    create_time = Column(DateTime, default=datetime.now, comment="创建时间")
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")
    is_deleted = Column(Integer, default=1, comment="是否删除，默认未删除")
    __table_args__ = ({'comment': '用例执行记录主表'})


class TestCaseExecutionRecord(Base):
    """
    用例执行记录详情表
    """
    __tablename__ = "testcase_execution_record"
    id = Column(Integer, primary_key=True, autoincrement=True)
    testcase_id = Column(Integer, comment="关联用例id")
    result_id = Column(Integer, comment="关联执行记录主表id")
    status = Column(Integer, comment="用例执行状态")
    __table_args__ = ({'comment': '用例执行记录详情表'})


class LoadResource(Base):
    """施压机资源."""
    __tablename__ = 'load_resource'  # 数据库名字
    id = Column(Integer, primary_key=True, doc='主键', comment='主键')  # 压测资源主键，comment为列注释
    resource_ip = Column(String(50), doc='资源ip', comment='资源ip')  # 压测资源IP
    resource_zone = Column(String(50), doc='资源区域', comment='资源区域')  # 压测资源区域
    project_id = Column(String(250), doc='项目id', comment='项目id')  # 占用资源的项目ID
    scene_id = Column(String(250), doc='场景id', comment='场景id')  # 占用资源的场景ID
    task_name = Column(String(250))  # 占用资源的任务名字
    task_uid = Column(String(250), doc='任务id', comment='任务id')  # 占用资源的任务ID，根据任务ID可以得知项目和场景信息
    resource_status = Column(Boolean, default=False, doc='资源状态', comment='资源状态')  # 压测资源可用状态,默认False表示可用
    gmt_create = Column(DateTime, default=datetime.now, doc='创建时间', comment='创建时间')  # 创建时间
    gmt_modify = Column(DateTime, default=datetime.now, onupdate=datetime.now, doc='更新时间',
                        comment='更新时间')  # 修改时间
    __table_args__ = (
        Index('index(zone,status)', 'resource_zone', 'resource_status'), {'comment': '压测资源表'})  # 添加索引和表注释
