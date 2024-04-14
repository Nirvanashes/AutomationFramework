import logbook
from config import settings
from .decorator import SingletonDecorator


@SingletonDecorator
class Log(object):
    handler = None

    def __init__(self, name='AutomationFramework', filename=fr"{settings.log['path']}"):
        logbook.set_datetime_format("local")
        self.logger = logbook.Logger(name)
        self.handler = logbook.FileHandler(filename, encoding='utf-8')
        self.handler.push_application()

    def info(self, *args, **kwargs):
        return self.logger.info(*args, **kwargs)

    def error(self, *args, **kwargs):
        return self.logger.error(*args, **kwargs)

    def warning(self, *args, **kwargs):
        return self.logger.warning(*args, **kwargs)

    def debug(self, *args, **kwargs):
        return self.logger.debug(*args, **kwargs)
