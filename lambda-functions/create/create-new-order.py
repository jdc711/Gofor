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
table = dynamodb.Table("Order")

def req_valid(data):
    if "customer_id" not in data or "item_name" not in data:
        return False

def get_current_date():
    current_date_obj = datetime.now()
    current_date = current_date_obj.strftime("%Y%m%d") # ex: 20250411 for April 11 2025
    return current_date

def lambda_handler(event, context):
    data = json.loads(event["body"])
    if not req_valid(data):
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Missing required parameter"}),
        } 

    order_id  = str(uuid.uuid4())
    customer_id = data["customer_id"]
    item_name = data["item_name"]
    current_date = get_current_date()
     
    order = {
        "id": order_id,
        "status": "PENDING",
        "customer_id": user_id,
        "item_name": item_name
        "created_date": current_date
    }

    table.put_item(Item=user)

    return {
        "statusCode": 201,
        "body": json.dumps({"message": "Order created", "id": order_id}),
    }