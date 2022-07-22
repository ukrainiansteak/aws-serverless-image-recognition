import os
import json

import boto3

dynamodb_client = boto3.client("dynamodb")
TABLE_NAME = os.environ["TABLE_NAME"]

def handler(event, context):

    blob_id = event["path"]["blob_id"]

    result = dynamodb_client.get_item(
        TableName=TABLE_NAME,
        Key={"blob_id": {"S": blob_id}}).get("Item")

    if not result:
        return {
            "statusCode": 404, "body": json.dumps({
                "error": "Blob not found"
            })
        }

    labels = result.get("labels").get("SS")
    response_labels = []
    for label in labels:
        response_labels.append(json.loads(label))

    response = {
        "blob_id": blob_id,
        "labels": response_labels,
        "statusCode": 200
    }

    return response
