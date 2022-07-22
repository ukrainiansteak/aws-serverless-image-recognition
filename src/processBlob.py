import os
import json

import boto3

TABLE_NAME = os.environ["TABLE_NAME"]
BUCKET_NAME = os.environ["BUCKET_NAME"]
rekognition_client = boto3.client('rekognition')
dynamodb_client = boto3.client('dynamodb')

def handler(event, context):

    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    response = rekognition_client.detect_labels(
        Image={'S3Object':{'Bucket': bucket,'Name':key}},
        MaxLabels=10
    )

    # format detected labels into a list of dicts
    labels = []
    for label in response['Labels']:
        labels.append(str(json.dumps({
            "label": label['Name'],
            "confidence": label['Confidence'],
            "parents": [parent["Name"] for parent in label['Parents']]
        })))

    result = dynamodb_client.get_item(
        TableName=TABLE_NAME,
        Key={"blob_id": {"S": key}}).get('Item')

    item = {
        'blob_id': {"S": key},
        'callback_url': {"S": result['callback_url']['S']},
        'labels': {"SS": labels}
    }

    dynamodb_client.put_item(
        TableName=TABLE_NAME,
        Item=item)

    return json.dumps(
        {
            "statusCode": 201,
        }
    )
