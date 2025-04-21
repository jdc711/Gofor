import json
import boto3
from boto3.dynamodb.conditions import Key, Attr

# Get the service resource.
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('UserLogin')

def handler (event, context):
    statusCode = 200
    headers = {
        "Content-Type": "application/json"
    }

    print(event)

