import os
import json
import uuid
import re

import boto3
from botocore.exceptions import ClientError
from botocore.config import Config

dynamodb_client = boto3.client("dynamodb")
s3_client = boto3.client('s3', config=Config(signature_version='s3v4'))
TABLE_NAME = os.environ["TABLE_NAME"]
BUCKET_NAME = os.environ["BUCKET_NAME"]

def handler(event, context):

    event_body = event['body']

    if not event_body:
        return {
            "statusCode": 400, "body": json.dumps({
                "error": "body is empty"
            })
        }

    callback_url = json.loads(event_body)["callback_url"]
    pattern = r'[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b'
    if not callback_url or not re.search(pattern, callback_url):
        return {
            "statusCode": 400,
            "body": json.dumps({
                "error": "Invalid callback url supplied"
            })
        }

    blob_id = str(uuid.uuid4())

    dynamodb_client.put_item(
        TableName=TABLE_NAME,
        Item={
            'blob_id': {"S": blob_id},
            'callback_url': {"S": callback_url}
        }
    )

    try:
        upload_url = s3_client.generate_presigned_url(
            ClientMethod='put_object',
            Params={
                'Bucket': BUCKET_NAME,
                'Key': f"{blob_id}"
            },
            ExpiresIn=3600,
            HttpMethod = 'PUT'
        )
    except ClientError as e:
        print(e)
        return {
            "statusCode": 500,
        }

    return {
        "statusCode": 201,
        "body": json.dumps(
            {
                "blob_id": blob_id,
                "upload_url": upload_url
            }
        )
    }
