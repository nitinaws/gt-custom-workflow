import json
import base64
from urllib.parse import urlparse
import boto3


def lambda_handler(event, context):
    """Sample PreHumanTaskLambda ( pre-processing lambda) for custom labeling jobs.
    For custom AWS SageMaker Ground Truth Labeling Jobs, you have to specify a PreHumanTaskLambda (pre-processing lambda).
    AWS SageMaker invokes this lambda for each item to be labeled. Output of this lambda, is merged with the specified
    custom UI template. This code assumes that specified custom template have only one placeholder "taskObject".
    If your UI template have more parameters, please modify output of this lambda.
    Parameters
    ----------
    event: dict, required
        Content of event looks some thing like following
        {
           "version":"2018-10-16",
           "labelingJobArn":"<your labeling job ARN>",
           "dataObject":{
              "source-ref":"s3://<your bucket>/<your keys>/awesome.jpg"
           }
        }
        As SageMaker product evolves, content of event object will change. For a latest version refer following URL
        Event doc: https://docs.aws.amazon.com/sagemaker/latest/dg/sms-custom-templates-step3.html
    context: object, required
        Lambda Context runtime methods and attributes
        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html
    Returns
    ------
    output: dict
        This output is an example JSON. We assume that your template have only one placeholder named "taskObject".
        If your template have more than one placeholder, make sure to add one more attribute under "taskInput"
        {
           "taskInput":{
              "taskObject":src_url_http
           },
           "isHumanAnnotationRequired":"true"
        }
        Note: Output of this lambda will be merged with the template, you specify in your labeling job.
        You can use preview button on SageMaker Ground Truth console to make sure merge is successful.
        Return doc: https://docs.aws.amazon.com/sagemaker/latest/dg/sms-custom-templates-step3.html
    """

    # Event received
    print("Received event: " + json.dumps(event, indent=2))

    # Get source if specified
    source = event['dataObject']['source'] if "source" in event['dataObject'] else None

    # Get source-ref if specified
    source_ref = event['dataObject']['source-ref'] if "source-ref" in event['dataObject'] else None

    metadata = event['dataObject']['metadata'] if "metadata" in event['dataObject'] else None


    text_file_s3_uri = event['dataObject']['text-file-s3-uri'] if "text-file-s3-uri" in event['dataObject'] else None

    # if source field present, take that otherwise take source-ref
    task_object = source if source is not None else source_ref

    # Build response object
    output = {
        "taskInput": {
            "taskObject": task_object
        },
        "isHumanAnnotationRequired": "true"
    }

    if metadata is not None:
        # Add s3 URI for text file to metadata so it is preserved in output
        output['taskInput']['metadata'] = metadata

    if text_file_s3_uri is not None:
        print(text_file_s3_uri)
        output['taskInput']['text'] = getText(text_file_s3_uri)

    print(output)
    # If neither source nor source-ref specified, mark the annotation failed
    if task_object is None:
        print(" Failed to pre-process {} !".format(event["labelingJobArn"]))
        output["isHumanAnnotationRequired"] = "false"

    return output


def getText(s3uri):
    # Get S3 object and return text
    o = urlparse(s3uri)
    bucket = o.netloc
    key = o.path.lstrip('/')
    text = ""
    boto3.client('s3')
    s3 = boto3.resource('s3')
    try:
        obj = s3.Object(bucket, key);
        text = obj.get()['Body'].read().decode('utf8')
        return text
    except:
        print("The object does not exist.")
        raise

    return text


