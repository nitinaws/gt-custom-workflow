import json
import boto3
from urllib.parse import urlparse

def lambda_handler(event, context):

    consolidated_labels = []
    print("Event: {}".format(event))
    parsed_url = urlparse(event['payload']['s3Uri'])
    s3 = boto3.client('s3')

    textFile = s3.get_object(Bucket = parsed_url.netloc, Key = parsed_url.path[1:])

    filecont = textFile['Body'].read()

    annotations = json.loads(filecont)
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
                        'claims_info': new_annotation,
                        'ddb_id': dataset['dataObject']['content']
                        }
                    }
                }
            }
            consolidated_labels.append(label)

    print("Response:{}".format(json.dumps(consolidated_labels)))

    return consolidated_labels