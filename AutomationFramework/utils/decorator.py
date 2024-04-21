"""
装饰器文件
"""
from curses import wrapper

from AutomationFramework.utils import user_token


class SingletonDecorator(object):
    def __init__(self, cls):
        self.cls = cls
        self.instance = None

    def __call__(self, *args, **kwargs):
        if self.instance is None:
            self.instance = self.cls(*args, **kwargs)
        return self.instance

#
# class permission():
#     def login_required(func):
#         @wrapper(func)
#         def wrapper(*args, **kwargs):
#             try:
#                 from urllib import request
#                 headers = request.headers
#                 token = headers.get('Authorization')
#                 if token is None:
#                     return {'message': 'Token is missing','code':401}
#                 user_info = user_token.parse_token(token)