import json
import boto3
import logging
from boto3.dynamodb.conditions import Key

# Connect to DynamoDB
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Item')

def handler(event, context):
    try:

        if event.get("httpMethod") != "GET":
            return  {
                "statusCode": 405,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"message": "Item not found with id"})
            }

        params = event.get("queryStringParameters") or {}
        item_id = params.get("id")

        if item_id:
            item = get_item_by_id(item_id)
            if not item:
                return  {
                    "statusCode": 404,
                    "headers": {"Content-Type": "application/json"},
                    "body": json.dumps({"message": "Item not found with id"})
                }
            return  {
                    "statusCode": 200,
                    "headers": {"Content-Type": "application/json"},
                    "body": json.dumps({"item": item})
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
def get_item_by_id(item_id):
    response = table.get_item(Key={"id": item_id})
    return response.get("Item")

