import json
import boto3
import logging
from boto3.dynamodb.conditions import Key

# Connect to DynamoDB
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Order')

def handler(event, context):
    try:

        if event.get("httpMethod") != "GET":
            return  {
                "statusCode": 405,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"message": "Order not found with id"})
            }

        params = event.get("queryStringParameters") or {}
        order_id = params.get("id")

        if order_id:
            order = get_order_by_id(order_id)
            if not order:
                return  {
                    "statusCode": 404,
                    "headers": {"Content-Type": "application/json"},
                    "body": json.dumps({"message": "Order not found with id"})
                }
            return  {
                    "statusCode": 200,
                    "headers": {"Content-Type": "application/json"},
                    "body": json.dumps({"order": order})
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
def get_order_by_id(order_id):
    response = table.get_item(Key={"id": order_id})
    return response.get("Item")

