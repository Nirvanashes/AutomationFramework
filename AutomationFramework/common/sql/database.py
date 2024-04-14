from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy.ext.declarative import declarative_base
from config import settings

# 数据库地址
SQLALCHEMY_DATABASE_URL = f"{settings.sqlite['path']}"
# 启动引擎
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# 启动会话
SessionLocal = sessionmaker(autocommit=False, bind=engine)


# 数据模型基类
Base = declarative_base()
