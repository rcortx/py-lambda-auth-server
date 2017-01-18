# lambda_function.py

import json

import middleware
import settings

def lambda_handler(event, context=None):
            """
            As all exceptions are delegated to the top layer, this function will handle them
                albiet, crudely for now with more information leak for testing purposes
            """
            response = {}
            try:
                response = middleware.IdentityAuthMiddleWare.process_request(event, response)
            except Exception as e:
                response["message"] = e.message
                response["errors"] = e.errors
                # removing request_dump data
                if "request_dump" in response["errors"]:
                        del response["errors"]["request_dump"]
                for _k, _v in response["errors"].items():
                    response["errors"][_k] = str(_v)
            return response
