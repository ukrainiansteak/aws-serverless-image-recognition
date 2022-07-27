import os
import json

import boto3

dynamodb_client = boto3.client("dynamodb")
TABLE_NAME = os.environ["TABLE_NAME"]

def handler(event, context):

    blob_id = event["path"].replace('/blobs/', "")

    result = dynamodb_client.get_item(
        TableName=TABLE_NAME,
        Key={"blob_id": {"S": blob_id}}).get("Item")

    if not result:
        return {
            "statusCode": 404,
            "body": json.dumps({
                "error": "Blob not found"
            })
        }

    try:
        labels = result.get("labels").get("SS")
        response_labels = []
        for label in labels:
            response_labels.append(json.loads(label))
    except AttributeError:
        return {
            "statusCode": 404,
            "body": json.dumps({
                "error": "Blob not found"
            })
        }

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "blob_id": blob_id,
                "labels": response_labels,
            }
        )
    }
