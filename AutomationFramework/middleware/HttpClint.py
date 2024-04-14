import requests
import datetime


class Request:
    def __init__(self, url, session=False, **kwargs):
        self.url = url
        self.session = session
        self.kwargs = kwargs
        if self.session:
            self.client = requests.Session()
            return
        self.client = requests

    @staticmethod
    def get_elapsed(timer: datetime.timedelta):
        if timer.seconds > 0:
            return f"{timer.seconds}.{timer.microseconds // 1000}s"
        return f"{timer.seconds // 100}ms"

    def get(self):
        return self.request(method="GET")

    def post(self):
        return self.request("POST")

    def request(self, method: str):
        status_code = 0
        elapsed = "-1ms"
        try:
            if method.upper() == "GET":
                response = self.client.get(self.url, **self.kwargs)
            elif method.upper() == "POST":
                response = self.client.post(self.url, **self.kwargs)
            else:
                response = self.client.request(self.url, **self.kwargs)
            status_code = response.status_code
            if status_code != 200:
                return Request.response(False, status_code)
            # elapsed = Request.get_elapsed(response.elapsed)
            elapsed = response.elapsed
            data = response.json()
            return Request.response(True, 200, data, response.headers, response.request.headers, elapsed=elapsed)
        except Exception as e:
            return Request.response(False, status_code, elapsed=elapsed, msg=str(e))

    @staticmethod
    def response(status, status_code=200, response=None, reponse_headers=None, requests_headers=None, msg="success",
                 elapsed=None):
        request_header = {k: v for k, v in requests_headers.items()}
        response_header = {k: v for k, v in reponse_headers.items()}
        return {
            'status': status,
            'status_code': status_code,
            'response': response,
            'request_header': request_header,
            'response_header': response_header,
            'elapsed': elapsed,
            'message': msg
        }
