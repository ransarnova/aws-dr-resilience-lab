import json
import os
import uuid
from datetime import datetime, timezone

import boto3
from botocore.exceptions import ClientError

REGION = os.environ["AWS_REGION"]
TABLE_NAME = os.environ["TABLE_NAME"]

dynamodb = boto3.resource("dynamodb", region_name=REGION)
table = dynamodb.Table(TABLE_NAME)


def response(status, body):
    return {
        "statusCode": status,
        "headers": {"content-type": "application/json"},
        "body": json.dumps(body),
    }


def lambda_handler(event, context):
    path = event.get("rawPath", "/")
    method = event.get("requestContext", {}).get("http", {}).get("method", "")

    if method == "GET" and path == "/health":
        return response(200, {"status": "healthy", "region": REGION})

    try:
        if method == "POST" and path == "/orders":
            order_id = str(uuid.uuid4())

            item = {
                "order_id": order_id,
                "status": "CREATED",
                "source_region": REGION,
                "created_at": datetime.now(timezone.utc).isoformat(),
            }

            table.put_item(Item=item)

            return response(201, item)

        if method == "GET" and path.startswith("/orders/"):
            order_id = path.removeprefix("/orders/")

            if not order_id:
                return response(400, {"message": "Missing order ID"})

            result = table.get_item(
                Key={"order_id": order_id},
                ConsistentRead=True,
            )

            item = result.get("Item")

            if not item:
                return response(404, {"message": "Order not found"})

            return response(200, item)

        return response(404, {"message": "Not found"})

    except ClientError:
        print("DynamoDB operation failed", flush=True)
        return response(503, {"message": "Service temporarily unavailable"})
