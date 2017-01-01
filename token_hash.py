# token_hash.py
import uuid
import calendar
import time 
import random 

def get_token_hash(token, *args):
    """hashes passed token using a salt"""
    salt = str(token) + str(calendar.timegm(time.gmtime())) + str(random.random())
    salt.encode('utf-8').strip()
    return str(uuid.uuid3(uuid.NAMESPACE_DNS, salt))