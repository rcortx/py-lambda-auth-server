# settings.py

URLS = {}
URLS['AUTH'] = "auth"
URLS['VIEWS'] = []

HEADER_KEY = "headers"

PAYLOAD_KEY = "body"

PARAM_KEY = "param"

URL_KEY = "url"

METHOD_KEY = "method"

AUTH = {}

#TOKEN
AUTH['TOKEN_HEADER'] = "auth-header"
AUTH['TOKEN_EXPIRY'] = 15*60
AUTH['USER_KEY'] = "user"
AUTH['TOKEN_TIME_KEY'] = "time"
AUTH['TOKEN_USER_KEY'] = "user"

# ALLOWED METHODS for AUTHENTICATION
AUTH['ALLOWED_METHODS'] = ['POST']

# CREDENTIALS
AUTH['CREDENTIALS_KEY_USER'] = "user"
AUTH['CREDENTIALS_KEY_SECRET'] = "secret"

SAFE_METHODS = ['GET', 'OPTIONS']

SAFE_CODES = [1, True]

DB = {
    "USERS":"users",
    "TOKENS":"tokens",
}