import unittest
import middleware
import custom_errors
import db
import authorizers
import token_hash
import settings

"""
NOTE: DEPRECATED UNIT-TESTS: Don't Run!
"""

class MiddleWareTest(unittest.TestCase):

    def test_processRequest_identityAuth(self):
        
        try:
            user = "U:100"
            secret = "top_secret"
            token = token_hash.get_token_hash(user)
            request = {"payload":
                            {settings.AUTH['CREDENTIALS_KEY_USER']: user,
                            settings.AUTH['CREDENTIALS_KEY_SECRET']: secret,},
                    "method":'POST',
                    "url":"auth/",#"auth/"
                    "header":{"test_header":"U:100"}
                    }
            response = {}
            result = middleware.IdentityAuthMiddleWare.process_request(request, response)
            expected = {"test_header":user}
            self.assertEqual(expected, result)
        except custom_errors.AuthError as e:
            print e.errors
            self.assertEqual(None, None)

    def test_processRequest_hiddenViews(self):
        
        try:
            user = "U:100"
            secret = "top_secret"
            token = 'U:100'#token_hash.get_token_hash(user)
            request = {"payload":
                            {settings.AUTH['CREDENTIALS_KEY_USER']: user,
                            settings.AUTH['CREDENTIALS_KEY_SECRET']: secret,},
                    "method":'POST',
                    "url":"test1/",#"auth/"
                    "header":{"test_header":"U:100"}
                    }
            response = {}
            result = middleware.IdentityAuthMiddleWare.process_request(request, response)
            expected = {"test_header":user}
            self.assertEqual(expected, result)
        except custom_errors.AuthError as e:
            print e.errors
            self.assertEqual(None, None)


    def test_processRequest_cyclic(self):
            user = "U:1"
            secret = "secret"
            token = 'U:100'#token_hash.get_token_hash(user)
            request = {"payload":
                            {settings.AUTH['CREDENTIALS_KEY_USER']: user,
                            settings.AUTH['CREDENTIALS_KEY_SECRET']: secret,},
                    "method":'POST',
                    "url":"auth/",#"auth/"
                    "headers":{"test_header":"U:100"}
                    }
            response = {}
            result = middleware.IdentityAuthMiddleWare.process_request(request, response)
            #print result
            
            expected = {settings.AUTH['TOKEN_HEADER']:user}
            token = result[settings.AUTH['TOKEN_HEADER']]
            request["headers"][settings.AUTH['TOKEN_HEADER']] = token

            request["url"] = "test-1/"
            result = middleware.IdentityAuthMiddleWare.process_request(request, response)
            self.assertEqual(expected, result)
            except Exception as e:#custom_errors.AuthError
                print e.message
                print e.errors
            self.assertEqual(None, None)

    def test_processRequest_viewAuth(self):
        user = "U:100"
        secret = "top_secret"
        token = token_hash.get_token_hash(user)
        request = {"payload":
                            {settings.AUTH['CREDENTIALS_KEY_USER']: user,
                            settings.AUTH['CREDENTIALS_KEY_SECRET']: secret,},
                    "method":'GET',
                    "url":"auth/",#"auth/"
                    "header":{"test_header":"U:100"}
                    }
        response = {}
        try:
            result = middleware.ViewAuthMiddleWare.process_request(request, response)
            expected = "view_auth_response"
            self.assertEqual(expected, result)
        except custom_errors.AuthError as e:
            print e.errors
            self.assertEqual(None, None)
            

class AuthErrorTest(unittest.TestCase):
    def test_authError_raisingWithAmbientDict(self):
        seed_info = {"custom_error_info":"ambient error info"}
        try:
            raise custom_errors.AuthError("This is a demo AuthError", seed_info)
        except custom_errors.AuthError as e:
            print e.message
            print e.errors 
            self.assertEqual(seed_info, e.errors)

    def test_bundleError_raisingWithAmbientDict(self):
        seed_info = {"custom_error_info":"bundle error info"}
        try:
            raise custom_errors.ImproperErrorBundleDump("This is a demo BundleError", seed_info)
        except custom_errors.ImproperErrorBundleDump as e:
            print e.message
            print e.errors 
            self.assertEqual(seed_info, e.errors)

    def test_customError_bundle(self):
        res = custom_errors.CustomError.bundle(["test1", "test2"], "val_test1", "val_test2")
        expected = {"test1":"val_test1", "test2":"val_test2"}
        self.assertEqual(expected, res)


class DBTest(unittest.TestCase):
    def test_dbAdapter_getandset(self):
        dbase = db.DBAdapter.get_instance(db.DummyDBWrapper)
        key = "TEst_key"
        value = "tyes_value"
        dbase.set(key, value)
        res = dbase.get(key)
        self.assertEqual(value, res)

class AuthTest(unittest.TestCase):
    def test_authorizer_errosFormat(self):
        expected = {1: "This method is not allowed for authentication! Only "+\
                        " %s methods are allowed!"%(['POST']),
                    2: "Authentication failed! Auth details provided are incorrect!",
                    3: "User is not authenticated! Please sign-in!"}
        self.assertEqual(expected, authorizers.Authenticator.ERRORS)

    def test_authorizer_authorize(self):
        user = "U:100"
        secret = "top_secret"
        token = token_hash.get_token_hash(user)
        auth = authorizers.Authenticator()
        request = {"payload":
                            {settings.AUTH['CREDENTIALS_KEY_USER']: user,
                            settings.AUTH['CREDENTIALS_KEY_SECRET']: secret,},
                    "method":'POST',
                    "url":"aut",#"auth/"
                    "header":{"test_header":"U:100"}
                    }
        res = auth.authorize(request)
        print res
        self.assertEqual(True, res[0])

#if __name__ == "__main__": unittest.main()

