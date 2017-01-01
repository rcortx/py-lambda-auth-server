# custom_errors.py

# custom error class which enables extra ambient detail passing
class CustomError(Exception):
    def __init__(self, message, errors):
        """
        @param: message: string, error message
        @param: errors: dict, dictionary of error ambient details
        """
        super(CustomError, self).__init__(message)
        # stores dict of error information in .errors attribute
        self.errors = errors

    @staticmethod
    def bundle(bundle_keys, *args):
        lim = len(bundle_keys)
        if len(args) != lim:
            raise ImproperErrorBundleDump(ImproperErrorBundleDump.MSG_IMPROPER_ERROR_BUNDLE_DUMP, 
                {"args":args, "keys":bundle_keys})
        bundle = {}
        for i in range(lim):
            bundle[bundle_keys[i]] = args[i]
        return bundle


# custom error class for Auth Failure
class AuthError(CustomError):
    MSG_AUTH_FAILED = "Auth failed!"


# custom error class for Improper Error Bundle Dump
class ImproperErrorBundleDump(CustomError):
    MSG_IMPROPER_ERROR_BUNDLE_DUMP = "Insufficient Info! Incorrect number of parameters passed to Error Dump!"

class AbstractMiddlewareError(CustomError):
    MSG_ABS_MIDDLEWARE_ERROR = "An abstract middleware can't be processed!"

class Resource404(CustomError):
    MSG_404 = "Requested URL was not found on the server!"