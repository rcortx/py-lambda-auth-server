# db.py
import abc
from boto3.dynamodb.conditions import Key
import boto3

from utils import classonlymethod


class AbstractDBWrapper(object):
    """
    Abstract class for a database wrapper interface
        simulates NoSQL behaviour
    """
    _metaclass_ = abc.ABCMeta

    @abc.abstractmethod
    def open(self):
        """
        Opens connection to the database
        """
        return

    @abc.abstractmethod    
    def close(self):
        """
        Closes connection to the database
        """
        return

    @abc.abstractmethod    
    def get(self, model, key):
        """
        Returns value of key
        """
        return

    @abc.abstractmethod    
    def set(self, model, value):
        """
        Assigns provided value to key
        """
        return


class DynamoDBWrapper(AbstractDBWrapper):
    """
    wrapper over dynamodb in AWS
    """
    models = {
        "users": None,
        "tokens": None,
    }
    
    def open(self):
        dynamo = boto3.resource('dynamodb')
        self.models["users"] = dynamo.Table('users_test')
        self.models["tokens"] = dynamo.Table('tokens')
    
    def close(self):
        pass
    
    def set(self, table, item):
        self.models[table].put_item(
           Item=item
            )
    
    def get_item_npk(self, table, key, value, index=None):
            if not index:
                index = key + "-index"
            return self.models[table].query(
                IndexName=index,
                 KeyConditionExpression=Key(key).eq(value))["Items"][0]
        
    def get(self, table, key):
            key = {table[:-1]:key}
            """key represents primary key"""
            return self.models[table].get_item(
                Key=key
                )["Item"]
    
    def check_v(self, table, key, expected):
        res = self.get_item_npk(table, table[:-1], key)
        for _k, _v in expected.items():
            if res[_k] != _v:
                return False
        return True


class DBAdapter(object):
    _instance = None # static instance of class
    
    @property # refers to the database object
    def db(self):
        return self._db
    
    @db.setter
    def db(self, dbWrapper):
        self._db = dbWrapper()
        self._db.open()
    
    @db.deleter
    def db(self):
        self._db.close()

    @classonlymethod
    def get_instance(cls, dbWrapper=None):
        """Returns singleton instance of this class
        @param: dbWrapper: concrete class inheriting from abstract class AbstractDBWrapper
        """
        if not cls._instance:
            if not dbWrapper:
                dbWrapper = DynamoDBWrapper
            cls._instance = cls(dbWrapper)
        return cls._instance

    def __init__(self, dbWrapper):
        """Never use directly!"""
        self.db = dbWrapper

    def get(self, model, key):
        return self.db.get(model, key)

    def set(self, model, value):
        self.db.set(model, value)

    def check_value(self, model, key, expected):
        return self.db.check_v(model, key, expected)


class DummyDBWrapper(AbstractDBWrapper):
    """
    **DEPRECATED dummy wrapper for testing purposes
    """
    _db_sim = {
        "users":{"U:100":"top_secret"},
        "tokens":{
            "U:100":{
                "user":"U:100",
                "time":1483189400,
                }
        }} # test user and secret

    def open(self):
        pass
    
    def close(self):
        pass
    
    def get(self, model, key):
        p_key = key["primary"]
        if p_key in self._db_sim[model]:
            return self._db_sim[model][p_key]
        return None 
    
    def set(self, model, value):
        self._db_sim[model][value["primary"]] = value


def test(): # ignore this
    settings = {
        "DB":{
            "TOKENS":"tokens",
            'TOKEN_TIME_KEY':'time',
            'TOKEN_USER_KEY': 'user',
            "USERS": 'users',
        },
        "AUTH":{
            'TOKEN_USER_KEY': 'user',
            'TOKEN_TIME_KEY': 'time',
        },
    }
    dbase = DBAdapter.get_instance()
    
    #################
    cur_time = 2313213
    token = "xxx"
    user = "U:100"
    secret = "secret"
    dbase.set(settings['DB']["USERS"], {"user_id":'10', "secret":secret, "user":user})

    # dbase.set()
    dbase.set(settings['DB']["TOKENS"], {settings['DB']["TOKENS"][:-1]:token, settings['AUTH']['TOKEN_USER_KEY']: user, 
                settings['AUTH']['TOKEN_TIME_KEY']: str(cur_time)})
    # dbase.get()
    fetched = dbase.get(settings['DB']["TOKENS"], token)# 2: {"primary":token}
    print fetched
    # dbase.check_value("")
    print dbase.check_value(settings['DB']["USERS"], user, {"secret":secret})

