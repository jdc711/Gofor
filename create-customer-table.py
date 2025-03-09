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
table = dynamodb.Table("Customer")

def lambda_handler(event, context):
    data = json.loads(event["body"])
    customer_id = str(uuid.uuid4())

    # validation
     
    customer = {
        "id": customer_id,
        "name": data.get("name"),
        "email": data.get("email"),
        "password": data.get("password"), 
    }

    table.put_item(Item=customer)

    return {
        "statusCode": 201,
        "body": json.dumps({"message": "Customer created", "customerId": customer_id}),
    }