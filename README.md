# Image Recognition API 

![diagram](https://test-task-image-perfsys.s3.eu-central-1.amazonaws.com/Untitled+Diagram.png)


## Use Cases

Label image recognition using AWS Rekognition. 

Client makes a ```POST``` request containing a ```callback_url``` as a request body parameter to ```/blobs``` API Endpoint. AWS Lambda function generates blob uuid and stores it together with ```callback_url``` in a DynamoDB table. The function returns response with an ```upload_url``` to an S3 Bucket. 

Once Client uploads the image using ```upload_url```, Lambda function is called. Image is processed by AWS Rekognition and DynamoDB blob record is updated with label info. 

Once DynamoDB blob record is updated, a function to make callback is triggered. It sends the label information to the callback_url specified by Client. 

Client can also make a GET request containing ```blob_id``` to the ```/blobs/{blob_id}``` endpoint to receive the information about the existing blob. 

## API Endpoints: 

```
POST /blobs
```
Accepts callback_url for receiving callback when recognition will be ended, and returns upload_url for uploading pictures

**Request Parameters:**
```callback_url```

**Response Parameters:** 
```upload_url```

---
```
GET /blobs/{blob_id}
``` 
Returns information about recognition results for specified blob 

**Request Parameters:**
```blob_id```

**Response Parameters:** 
```blob_id```
```labels```

## Deploy to AWS

```
$ sls deploy
```

### Example POST Request

```
curl -X POST https://xxxxxxxxxxxx.amazonaws.com/dev/blobs -d '{"callback_url": "example.com"}' -H "Content-Type: application/json"
```

### Example GET Request
```
curl -X GET https://xxxxxxxxxxxx.amazonaws.com/dev/blobs/blob_id 
```
