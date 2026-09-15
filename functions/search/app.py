import os
import json
import boto3

table = boto3.resource("dynamodb").Table(os.environ["TABLE_NAME"])


def handler(event, context):
    query = event.get("queryStringParameters") or {}
    title = query.get("title")

    if title:
        response = table.scan(
            FilterExpression="contains(fileId, :t)",
            ExpressionAttributeValues={":t": title}
        )
    else:
        response = table.scan()

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(response["Items"])
    }
