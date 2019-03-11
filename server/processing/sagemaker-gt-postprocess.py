import json
import boto3
from urllib.parse import urlparse

def lambda_handler(event, context):
    # Main lambda handler to create consolidated labels
    consolidated_labels = []
    print("Event: {}".format(event))
    s3 = boto3.client('s3')

    try:
        parsed_url = urlparse(event['payload']['s3Uri'])

        textFile = s3.get_object(Bucket = parsed_url.netloc, Key = parsed_url.path[1:])

        filecontent = textFile['Body'].read()

        annotations = json.loads(filecontent)
        print("Input annotations:{}".format(annotations))

        for dataset in annotations:
            for annotation in dataset['annotations']:
                new_annotation = json.loads(annotation['annotationData']['content'])
                label = {
                    'datasetObjectId': dataset['datasetObjectId'],
                    'consolidatedAnnotation' : {
                    'content': {
                        event['labelAttributeName']: {
                            'workerId': annotation['workerId'],
                            'annotations': new_annotation,
                            'entry': dataset['dataObject']['content']
                            }
                        }
                    }
                }
                consolidated_labels.append(label)

        print("Response:{}".format(json.dumps(consolidated_labels)))
    except:
        raise Exception

    return consolidated_labels