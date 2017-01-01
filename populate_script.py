# populate_script.py
import boto3

"""
For creating new users for tesing purposes
"""

def respond(err, res=None): # dummy
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }

def lambda_handler(event, context):
        dynamodb = boto3.resource('dynamodb')

        table = dynamodb.Table('users_test')
        
        def add_item(table, item):
            table.put_item(
           Item=item
            )
        item = event["body"]
        add_item(table, item)
        return {"status":"Success!"}
        
        """ Acceptable Format
        {"user_id": "U:2"
        "user": "lovely"
        "secret":"test-pass"}
        """