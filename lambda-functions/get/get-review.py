import json
import boto3
import logging
from boto3.dynamodb.conditions import Key

# Connect to DynamoDB
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Review')

def handler(event, context):
    try:

        if event.get("httpMethod") != "GET":
            return  {
                "statusCode": 405,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"message": "Review not found with id"})
            }

        params = event.get("queryStringParameters") or {}
        review_id = params.get("id")

        if review_id:
            review = get_review_by_id(review_id)
            if not review:
                return  {
                    "statusCode": 404,
                    "headers": {"Content-Type": "application/json"},
                    "body": json.dumps({"message": "Review not found with id"})
                }
            return  {
                    "statusCode": 200,
                    "headers": {"Content-Type": "application/json"},
                    "body": json.dumps({"review": review})
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
def get_review_by_id(review_id):
    response = table.get_item(Key={"id": review_id})
    return response.get("Item")

