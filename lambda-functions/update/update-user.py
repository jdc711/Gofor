import json
import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("User")

def valid_req(data):
    if "user_id" not in data:
        return False
    
    if ("latitude" in data and "longitude" not in data) or ("longitude" in data and "latitude" not in data):
        return False
    
    return True

 
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
    user_id = data["user_id"]

    update_expression = []
    expression_values = {}
    if "name" in data:
        update_expression.append("name = :name")
        expression_values[":name"] = data["name"]
    if "email" in data:
        update_expression.append("email = :email")
        expression_values[":email"] = data["email"]
    if "password" in data:
        update_expression.append("password = :password")
        expression_values[":password"] = data["password"]
    if "latitude" in data:
        update_expression.append("latitude = :latitude")
        expression_values[":latitude"] = float(data["latitude"])
        update_expression.append("longitude = :longitude")
        expression_values[":longitude"] = float(data["longitude"])

    if not update_expression:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "No valid fields to update"})
        }

    try:
        table.update_item(
            Key={"id": user_id},
            UpdateExpression="SET " + ", ".join(update_expression),
            ExpressionAttributeValues=expression_values
        )

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "User updated", "id": user_id}),
        }
    except Exception as e: 
        return {
            "statusCode": 500, 
            "body": json.dumps({"message": "Failed to update user", "error": str(e)})
        }

