# utils.py

# custom class onyl method decorator which forces a 
# method to be only callable from a class reference
# as opposed to an instance of the class

import settings

class classonlymethod(classmethod):
    def __get__(self, instance, owner):
        if instance is not None:
            raise AttributeError("This method is available only on the class and not an instance.")
        return super(classonlymethod, self).__get__(instance, owner) 



class RequestOp(object):
    """
    methods to extract various part s of the request object in required format
    (pluggable component for easy testing)
    """
    @staticmethod
    def getURL(request):
        return request[settings.URL_KEY]
    
    @staticmethod
    def getParam(request, key):
        return request[settings.PARAM_KEY][key]
    
    @staticmethod
    def getPayload(request, key):
        if key in request[settings.PAYLOAD_KEY]:
            return request[settings.PAYLOAD_KEY][key]
        return None
    
    @staticmethod
    def getHeader(request, key):
        if key in request[settings.HEADER_KEY]:
            return request[settings.HEADER_KEY][key]
        else: return None

    @staticmethod
    def getMethod(request):
        return request[settings.METHOD_KEY]

    @staticmethod
    def addParam(request, key, value):
        request[key] = value

    @staticmethod
    def appendParam(request, key, value):
        if not key in request:
            request[key] = [value]
        else:
            request[key].append(value)


