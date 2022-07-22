import os
import json
import urllib3
import boto3

dynamodb_client = boto3.client("dynamodb")
TABLE_NAME = os.environ["TABLE_NAME"]


def handler(event, context):

    blob_id = event["Records"][0]["dynamodb"]["Keys"]["blob_id"]["S"]

    result = dynamodb_client.get_item(
        TableName=TABLE_NAME,
        Key={"blob_id": {"S": blob_id}}).get("Item")

    if not result:
        return {
            "statusCode": 400, "body": json.dumps({
                "error": "No record with specified blob_id"
            })
        }

    labels = result.get("labels").get("SS")
    response_labels = []
    for label in labels:
        response_labels.append(json.loads(label))

    callback_url = result['callback_url']['S']
    data = {
        'blob_id': blob_id,
        'labels': response_labels
    }

    http = urllib3.PoolManager()

    response = http.request('POST',
                            callback_url,
                            body=json.dumps(data),
                            headers={'Content-Type': 'application/json'},
                            retries=False)

    return {
        "statusCode": 200
    }
