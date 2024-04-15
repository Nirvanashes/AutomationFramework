from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import settings

# 数据库地址
SQLALCHEMY_DATABASE_URL_SQLITE = f"{settings.sqlite['path']}"
SQLALCHEMY_DATABASE_URL_MYSQL = fr"{settings.database['driver']}+pymysql://{settings.database['db_user']}:{settings.database['db_password']}@{settings.database['db_host']}:{settings.database['db_port']}/{settings.database['db_name']}?charset='utf-8'"

# 启动引擎
engine = create_engine(SQLALCHEMY_DATABASE_URL_SQLITE, connect_args={"check_same_thread": False})
# engine = create_engine(SQLALCHEMY_DATABASE_URL_MYSQL,echo=True)

# 启动会话
SessionLocal = sessionmaker(autocommit=False, bind=engine)

# 数据模型基类
Base = declarative_base()
