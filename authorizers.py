# authorizers.py
import abc
import time
import calendar

from utils import classonlymethod, RequestOp
from token_hash import get_token_hash
import settings
import db


class AbstractAuthorizer(object):
    _metaclass_ = abc.ABCMeta

    @abc.abstractmethod
    def authorize(self, request):
        """
        @param: request -> the request dict object
        @return: list : ITEM[0] is AUTH CODE and is in settings.SAFE_CODES if 
            authorization was successful or not
        """
        return

    def __getattr__(self, name):
        try:
            return self.__dict[name]
        except KeyError:
            msg = "'{0}' object has no attribute '{1}'"
            raise AttributeError(msg.format(type(self).__name__, name))

    def __setattr__(self, name, value):
        self.__dict[name] = value



class SafeMethodOnlyAuthorizer(AbstractAuthorizer):
    ERROR_MSG = "This method is not safe! Only {} are allowed!".format(settings.SAFE_METHODS)
    ERROR_CODE = 10
    def authorize(self, request):
        if RequestOp.getMethod(request) in settings.SAFE_METHODS:
            return [True]
        return [self.ERROR_CODE, self.ERROR_MSG]


class Authenticator(AbstractAuthorizer):
    
    ERROR_CODE_METHOD_NOT_ALLOWED = 2
    ERROR_MSG_METHOD_NOT_ALLOWED = "This method is not allowed for authentication! Only" +\
        " %s methods are allowed!"%(settings.AUTH['ALLOWED_METHODS'])
    ERROR_CODE_AUTHENTICATION_FAILED = 3
    ERROR_MSG_AUTHENTICATION_FAILED = "Authentication failed! Auth details provided are incorrect!"
    ERROR_CODE_NOT_AUTHENTICATED = 4
    ERROR_MSG_NOT_AUTHENTICATED = "User is not authenticated! Please sign-in!"

    ERROR_CODE_AUTH_EXPIRED = 5
    ERROR_MSG_AUTH_EXPIRED = "Your authorization token has expired! Please re-login!"

    ERROR_CODE_NO_CREDENTIALS_SUPPLIED = 6
    ERROR_MSG_NO_CREDENTIALS_SUPPLIED = "There were no credentials supplied for authentication."

    ERRORS = {
                ERROR_CODE_METHOD_NOT_ALLOWED: ERROR_MSG_METHOD_NOT_ALLOWED,
                ERROR_CODE_AUTHENTICATION_FAILED: ERROR_MSG_AUTHENTICATION_FAILED,
                ERROR_CODE_NOT_AUTHENTICATED: ERROR_MSG_NOT_AUTHENTICATED,
                ERROR_CODE_AUTH_EXPIRED: ERROR_MSG_AUTH_EXPIRED,
                ERROR_CODE_NO_CREDENTIALS_SUPPLIED: ERROR_MSG_NO_CREDENTIALS_SUPPLIED
            }

    def authorize(self, request):
        if self.is_requesting_authentication(request):
            if not RequestOp.getMethod(request) in settings.AUTH['ALLOWED_METHODS']:
                return self.raise_error(self.ERROR_CODE_METHOD_NOT_ALLOWED)
            authentication = self.authenticate(request)
            if authentication: 
                request[settings.AUTH['TOKEN_HEADER']] = authentication
                return authentication
            return self.raise_error(self.ERROR_CODE_AUTHENTICATION_FAILED)
        else:
            authentication = self.is_authenticated(request)
            if authentication[0] in settings.SAFE_CODES:
                return [True]
            return self.raise_error(authentication[0])

    @staticmethod
    def is_requesting_authentication(request):
        return settings.URLS['AUTH'] == RequestOp.getURL(request)

    def authenticate(self, request):
        user = RequestOp.getPayload(request, settings.AUTH['CREDENTIALS_KEY_USER'])
        if not user:
            return False
        secret = RequestOp.getPayload(request, settings.AUTH['CREDENTIALS_KEY_SECRET'])
        dbase = db.DBAdapter.get_instance()
        #print "CRED DETAILS@@@@@ ", user, secret, dbase
        if dbase.check_value(settings.DB["USERS"], user, {"secret":secret}):# 2: {"primary":user}
            cur_time = calendar.timegm(time.gmtime())
            token = get_token_hash(user, cur_time)
            dbase.set(settings.DB["TOKENS"], {settings.DB["TOKENS"][:-1]:token, settings.AUTH['TOKEN_USER_KEY']: user, 
                settings.AUTH['TOKEN_TIME_KEY']: str(cur_time)})
            return (settings.SAFE_CODES[0], token)
        return False

    def is_authenticated(self, request):
        token = RequestOp.getHeader(request, settings.AUTH['TOKEN_HEADER'])
        if not token: return [self.ERROR_CODE_NO_CREDENTIALS_SUPPLIED]
        dbase = db.DBAdapter.get_instance()
        fetched = dbase.get(settings.DB["TOKENS"], token)# 2: {"primary":token}
        if not fetched:
            return [self.ERROR_CODE_NOT_AUTHENTICATED]
        cur_time = calendar.timegm(time.gmtime())
        if int(fetched[settings.AUTH['TOKEN_TIME_KEY']]) + settings.AUTH['TOKEN_EXPIRY'] > cur_time:
            request[settings.AUTH['USER_KEY']] = fetched[settings.AUTH['TOKEN_USER_KEY']]
            return [True]
        else: return [self.ERROR_CODE_AUTH_EXPIRED]

    @staticmethod
    def raise_error(code):
        return (code, Authenticator.ERRORS[code])


class APIAuthorizer(AbstractAuthorizer):
    def authorize(self, request):
        """As all APIs are accessible"""
        return [True]


class TestAuthorizer(AbstractAuthorizer):
    def authorize(self, request):
        return request["test_auth"]