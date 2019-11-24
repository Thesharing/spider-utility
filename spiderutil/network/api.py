from .session import Session

import sys

if sys.version_info[0] > 2:
    import urllib.parse as urlparse
else:
    import urlparse


class API(Session):

    def __init__(self, url: str, proxies=None, timeout=None, retry=None):
        Session.__init__(self, proxies=proxies, timeout=timeout, retry=retry)
        self.url = url

    class Callable:

        def __init__(self, session, name):
            self._session = session
            self._name = name

        def get(self, **kwargs):
            return self._session.get(urlparse.urljoin(self._session.url, self._name), **kwargs)

        def post(self, **kwargs):
            return self._session.post(urlparse.urljoin(self._session.url, self._name), **kwargs)

        def __getattr__(self, attr):
            return API.Callable(self._session, '{}/{}'.format(self._name, attr))

        def __getitem__(self, item):
            return self.__getattr__(item)

    def __getattr__(self, name):
        if '__' in name:
            return getattr(self.get, name)
        return API.Callable(self, name)

    def __getitem__(self, item):
        return self.__getattr__(item)
