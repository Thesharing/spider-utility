import requests
import sys

from .useragent import UserAgent
from ..exceptions import NullValueException, UnauthorizedException, \
    NetworkException, RetryLimitExceededException, SpiderException


class Session:
    """
    Session for using a
    """

    def __init__(self, proxies=None, timeout=None, retry=None):
        self.proxies = proxies
        self.timeout = timeout
        self.retry = retry
        self.session = requests.Session()

    @property
    def user_agent(self) -> str:
        return UserAgent.random()

    def request(self, method, url, **kwargs) -> requests.Response:
        """
        Package the request method in requests.
        :param url: URL address
        :param method: get/post method
        :param kwargs: the arguments like url, proxies, timeout, and etc
        :return: class `Response <Response>` object
        """
        retry = self.retry if self.retry else 1
        while retry > 0:
            try:
                if 'timeout' not in kwargs:
                    kwargs['timeout'] = self.timeout
                if 'proxies' not in kwargs:
                    kwargs['proxies'] = self.proxies
                r = method(url=url, **kwargs)
                if r.status_code == 200:
                    if len(r.content) > 0:
                        return r
                    else:
                        raise NullValueException(url)
                elif r.status_code == 401:
                    raise UnauthorizedException(url)
                else:
                    raise NetworkException(
                        'Error Code: {} - {}'.format(r.status_code, url))
            except (requests.exceptions.RequestException, SpiderException) as e:
                retry -= 1
                if retry <= 0:
                    if sys.version_info[0] > 2:
                        raise RetryLimitExceededException(url) from e
                    else:
                        raise

    def get(self, url, **kwargs) -> requests.Response:
        """
        HTTP GET Request
        :param url: URL address
        :param kwargs: network argument like proxies, timeout, and etc
        :return: class `Response <Response>` object
        """
        return self.request(self.session.get, url=url, **kwargs)

    def post(self, url, **kwargs) -> requests.Response:
        """
        HTTP POST Request
        :param url: URL address
        :param kwargs: network argument like proxies, timeout, and etc
        :return: class `Response <Response>` object
        """
        return self.request(self.session.post, url=url, **kwargs)
