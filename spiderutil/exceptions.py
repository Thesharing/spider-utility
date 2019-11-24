class SpiderException(Exception):

    def __init__(self, value=''):
        self.value = value

    def __str__(self):
        return self.value


class NetworkException(SpiderException):

    def __init__(self, value=''):
        super(NetworkException, self).__init__(value)
        self.msg = 'Network Error'


class RetryLimitExceededException(SpiderException):

    def __init__(self, value=''):
        super(RetryLimitExceededException, self).__init__(value)
        self.msg = 'Retry Limit Exceeded'


class UnauthorizedException(SpiderException):

    def __init__(self, value=''):
        super(UnauthorizedException, self).__init__(value)
        self.msg = 'Unauthorized request'


class NullValueException(SpiderException):

    def __init__(self, value=''):
        super(NullValueException, self).__init__(value)
        self.msg = 'Null value'


class NullPrimarySearchKeyException(SpiderException):

    def __init__(self, value=''):
        super(NullPrimarySearchKeyException, self).__init__(value)
        self.msg = 'Primary search key not specified.'


class AuthenticationFailedException(SpiderException):

    def __init__(self, value=''):
        super(AuthenticationFailedException, self).__init__(value)
        self.msg = 'Authentication Failed.'
