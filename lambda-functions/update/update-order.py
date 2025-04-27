import json
import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("Order")

def valid_req(data):
    if "order_id" not in data:
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
    order_id = data["order_id"]

    update_expression = []
    expression_values = {}
    if "status" in data:
        update_expression.append("status = :status")
        expression_values[":status"] = data["status"]
        if status == "DONE":
            delivered_date = get_current_date()
            update_expression.append("delivered_date = :delivered_date")
            expression_values[":delivered_date"] = data["delivered_date"]
    if "store_id" in data:
        update_expression.append("store_id = :store_id")
        expression_values[":store_id"] = data["store_id"]
    if "gofor_id" in data:
        update_expression.append("gofor_id = :gofor_id")
        expression_values[":gofor_id"] = data["gofor_id"]

    if not update_expression:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "No valid fields to update"})
        }

    try:
        table.update_item(
            Key={"id": order_id},
            UpdateExpression="SET " + ", ".join(update_expression),
            ExpressionAttributeValues=expression_values
        )

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Order updated", "id": order_id}),
        }
    except Exception as e: 
        return {
            "statusCode": 500, 
            "body": json.dumps({"message": "Failed to update order", "error": str(e)})
        }

