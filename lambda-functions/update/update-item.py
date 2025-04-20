import json
import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("Item")

def valid_req(data):
    if "item_id" not in data:
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
    item_id = data["item_id"]

    update_expression = []
    expression_values = {}
    if "name" in data:
        update_expression.append("name = :name")
        expression_values[":name"] = data["name"]
    if "store_id" in data:
        update_expression.append("store_id = :store_id")
        expression_values[":store_id"] = data["store_id"]
    if "price" in data:
        update_expression.append("price = :price")
        expression_values[":price"] = float(data["price"])

    if not update_expression:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "No valid fields to update"})
        }

    try:
        table.update_item(
            Key={"id": item_id},
            UpdateExpression="SET " + ", ".join(update_expression),
            ExpressionAttributeValues=expression_values
        )

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Item updated", "id": item_id}),
        }
    except Exception as e: 
        return {
            "statusCode": 500, 
            "body": json.dumps({"message": "Failed to update item", "error": str(e)})
        }

