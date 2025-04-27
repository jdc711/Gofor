'''
1) receive request and validate it
2) we will update ddb table using the request info
    - 
3) send response based on succcess/failiure
'''

import json
import boto3
import uuid
import time
from datetime import datetime


dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("Item")

def valid_req(data):
    if "store_id" not in data or "name" not in data or "price" not in data:
        return False
    return True

def lambda_handler(event, context):
    data = json.loads(event["body"])
    if not valid_req(data):
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Missing required parameter"}),
        } 

    item_id  = str(uuid.uuid4())
    name = data["name"]
    price = float(data["price"])
    store_id = data["store_id"]
     
    item = {
        "id": item_id,
        "name": name
        "price": price,
        "store_id": store_id
    }

    try:
        table.put_item(Item=item)

        return {
            "statusCode": 201,
            "body": json.dumps({"message": "Item created", "id": item_id}),
        }
    
    except Exception as e: 
        return {
            "statusCode": 500, 
            "body": json.dumps({"message": "Failed to create item", "error": str(e)})
        }