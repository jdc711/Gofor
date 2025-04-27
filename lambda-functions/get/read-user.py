import json
import boto3
import logging
from boto3.dynamodb.conditions import Key

# Connect to DynamoDB
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('User')

def handler(event, context):
    try:

        if event.get("httpMethod") != "GET":
            return  {
                "statusCode": 405,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"message": "User not found with id"})
            }

        params = event.get("queryStringParameters") or {}
        user_id = params.get("id")

        if user_id:
            user = get_user_by_id(user_id)
            if not user:
                return  {
                    "statusCode": 404,
                    "headers": {"Content-Type": "application/json"},
                    "body": json.dumps({"message": "User not found with id"})
                }
            return  {
                    "statusCode": 200,
                    "headers": {"Content-Type": "application/json"},
                    "body": json.dumps({"user": user})
                }

        else:
            return  {
                "statusCode": 400,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"message": "Missing 'id' parameter"})
            }
    except Exception as e:
        return {
            "statusCode": 500, 
            "body": json.dumps({"message": "Internal server error", "error": str(e)})
        }
def get_user_by_id(user_id):
    response = table.get_item(Key={"id": user_id})
    return response.get("Item")

