id!
customer id!
gofor id!
desc!
Rating!
created_date!


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
table = dynamodb.Table("Review")

def valid_req(data):
    if "customer_id" not in data or "gofor_id" not in data or "desc" not in data or "rating" not in data:
        return False

def get_current_date():
    current_date_obj = datetime.now()
    current_date = current_date_obj.strftime("%Y%m%d") # ex: 20250411 for April 11 2025
    return current_date

def lambda_handler(event, context):
    data = json.loads(event["body"])
    if not valid_req(data):
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Missing required parameter"}),
        } 

    review_id  = str(uuid.uuid4())
    customer_id = data["customer_id"]
    gofor_id = data["gofor_id"]
    desc = data["desc"]
    rating = float(data["rating"])
    current_date = get_current_date()
         
    review = {
        "id": order_id,
        "status": "PENDING",
        "customer_id": user_id,
        "item_name": item_name
        "created_date": current_date
    }

    try:
        table.put_item(Item=review)

        return {
            "statusCode": 201,
            "body": json.dumps({"message": "Review created", "id": review_id}),
        }
    
    except Exception as e: 
        return {
            "statusCode": 500, 
            "body": json.dumps({"message": "Failed to create review", "error": str(e)})
        }