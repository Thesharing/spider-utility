import requests
import sys

from .useragent import UserAgent
from ..exceptions import *


class Session:

    def __init__(self, proxies=None, timeout=None, retry=None):
        self.proxies = proxies
        self.timeout = timeout
        self.retry = retry
        self.session = requests.session()

    @property
    def user_agent(self):
        return UserAgent.random()

    def request(self, method, **kwargs):
        retry = self.retry if self.retry else 1
        while retry > 0:
            try:
                r = method(timeout=self.timeout, proxies=self.proxies, **kwargs)
                if r.status_code == 200:
                    if len(r.content) > 0:
                        return r
                    else:
                        raise NullValueException()
                elif r.status_code == 401:
                    raise UnauthorizedException()
                else:
                    raise NetworkException('Error Code: {}'.format(r.status_code))
            except (requests.exceptions.RequestException, SpiderException) as e:
                retry -= 1
                if retry <= 0:
                    if sys.version_info[0] > 2:
                        raise RetryLimitExceededException() from e
                    else:
                        raise

    def get(self, url, **kwargs):
        return self.request(self.session.get, url=url, **kwargs)

    def post(self, url, **kwargs):
        return self.request(self.session.post, url=url, **kwargs)
