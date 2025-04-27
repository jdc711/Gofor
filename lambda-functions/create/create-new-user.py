'''
1) receive request and validate it
2) we will update ddb table using the request info
    - 
3) send response based on succcess/failiure
'''

import json
import boto3
import uuid

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("User")

def valid_req(data):
    if "name" not in data or "email" not in data or "password" not in data:
        return False
    return True

def lambda_handler(event, context):
    data = json.loads(event["body"])

    if not valid_req(data):
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Missing required parameter"}),
        } 

    user_id = str(uuid.uuid4())
    name = data["name"]
    email = data["email"]
    password = data["password"]
     
    user = {
        "id": user_id,
        "name": name,
        "email": email,
        "password": password, 
    }

    try:
        table.put_item(Item=user)
        return {
            "statusCode": 201,
            "body": json.dumps({"message": "User created", "id": user_id}),
        }

    except Exception as e: 
        return {
            "statusCode": 500, 
            "body": json.dumps({"message": "Failed to create user", "error": str(e)})
        }

    