# lambda_function.py

import json

import middleware
import settings

def lambda_handler(event, context=None):
            response = {}
            try:
                response = middleware.IdentityAuthMiddleWare.process_request(event, response)
            except Exception as e:
                response["message"] = e.message
                response["errors"] = e.errors
                
                # removing request_dump data
                del response["errors"]["request_dump"]
                for _k, _v in response["errors"].items():
                    response["errors"][_k] = str(_v)
            return response
