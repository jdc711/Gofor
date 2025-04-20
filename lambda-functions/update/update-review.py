import json
import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("Review")

def valid_req(data):
    if "review_id" not in data:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Missing required parameter"})
        }
 
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
    review_id = data["review_id"]

    update_expression = []
    expression_values = {}
    if "desc" in data:
        update_expression.append("desc = :desc")
        expression_values[":desc"] = data["desc"]

    if not update_expression:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "No valid fields to update"})
        }

    try:
        table.update_item(
            Key={"id": review_id},
            UpdateExpression="SET " + ", ".join(update_expression),
            ExpressionAttributeValues=expression_values
        )

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Review updated", "id": review_id}),
        }
    except Exception as e: 
        return {
            "statusCode": 500, 
            "body": json.dumps({"message": "Failed to update review", "error": str(e)})
        }

