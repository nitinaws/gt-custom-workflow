import boto3
import json
import base64
from urllib.parse import urlparse

def lambda_handler(event, context):
    # Main lambda handler that formats input manifest entry into task input
    print(event)
    source = json.loads(event['dataObject']['source'])
    print('source :{}'.format(source))

    image_url = source['image_file']
    text = getText(source['text_file'])
    metadata = source['metadata']

    response = {
        "taskInput": {
            "image_url" : image_url,
            "text"  : text,
            "metadata": metadata
        }
    };

    print(response)
    return response



def getText(s3uri):
    # Get S3 object and return text
    o = urlparse(s3uri)
    bucket = o.netloc
    key = o.path.lstrip('/')

    boto3.client('s3')
    s3 = boto3.resource('s3')
    try:
        obj = s3.Object(bucket,key);
        text = obj.get()['Body'].read().decode('utf8')
        return text;
    except ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise

    return text