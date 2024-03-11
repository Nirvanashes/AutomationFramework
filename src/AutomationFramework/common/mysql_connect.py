from sqlalchemy import create_engine
from config import settings
from sqlalchemy.orm import sessionmaker


class MySQLConnect(object):
    def __init__(self):
        self.data = None
        self.tablename = None
        engine = create_engine(fr"{settings.database['driver']}+pymysql://"
                               f"{settings.database['db_user']}:{settings.database['db_password']}"
                               f"@{settings.database['db_host']}:{settings.database['db_port']}"
                               f"/{settings.database['db_name']}?charset='utf-8'",
                               echo=True)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def select_all(self, data, tablename):
        self.data = data
        self.tablename = tablename
        result = self.session.query(tablename).all()
