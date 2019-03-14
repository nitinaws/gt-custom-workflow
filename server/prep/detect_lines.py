import webbrowser, os
import json
import boto3
import io
import time
from io import BytesIO
import sys
from pprint import pprint
from urlparse import urlparse

# get the results
client = boto3.client(
    service_name='textract',
    region_name='us-east-1',
    endpoint_url='https://textract.us-east-1.amazonaws.com',
)



def get_rows_columns_map(table_result, blocks_map):
    rows = {}
    for relationship in table_result['Relationships']:
        if relationship['Type'] == 'CHILD':
            for child_id in relationship['Ids']:
                cell = blocks_map[child_id]
                if cell['BlockType'] == 'CELL':
                    row_index = cell['RowIndex']
                    col_index = cell['ColumnIndex']
                    if row_index not in rows:
                        # create new row
                        rows[row_index] = {}

                    # get the text value
                    rows[row_index][col_index] = get_text(cell, blocks_map)
    return rows


def get_text(result, blocks_map):
    text = ''
    if 'Relationships' in result:
        for relationship in result['Relationships']:
            if relationship['Type'] == 'CHILD':
                for child_id in relationship['Ids']:
                    word = blocks_map[child_id]
                    if word['BlockType'] == 'WORD':
                        text += word['Text'] + ' '
    return text


def get_table_csv_results(bucket,key):

    response = client.start_document_text_detection(DocumentLocation={"S3Object": {
              "Bucket": bucket,
              "Name": key }})

    jobid=response['JobId']


    job_response = client.get_document_text_detection(JobId=jobid)

    while job_response['JobStatus'] == 'IN_PROGRESS':
        time.sleep(15)
        job_response = client.get_document_text_detection(JobId=jobid)

    if job_response['JobStatus'] == 'SUCCEEDED' or job_response['JobStatus'] == 'PARTIAL_SUCCESS':
        blocks = job_response['Blocks']
    else:
        raise exception


    table_blocks = []
    blocks_map = {}
    for block in blocks:
        blocks_map[block['Id']] = block
        if block['BlockType'] == "LINE":
            #pprint(block)
            table_blocks.append(block)

    if len(table_blocks) <= 0:
        return "<b> NO Table FOUND </b>"

    csv = ''
    for index, table in enumerate(table_blocks):
        csv += generate_table_csv_2(table, blocks_map, index + 1)
        csv += '\n\n'

    return csv


def generate_table_csv(table_result, blocks_map, table_index):
    rows = get_rows_columns_map(table_result, blocks_map)

    table_id = 'Table_' + str(table_index)

    # get cells.
    csv = 'Table: {0}\n\n'.format(table_id)

    for row_index, cols in rows.items():

        for col_index, text in cols.items():
            csv += '{}'.format(text) + ","
        csv += '\n'

    csv += '\n\n\n'
    return csv

def generate_table_csv_2(table_result, blocks_map, table_index):

    table_id = 'Line_' + str(table_index)

    # get cells.
    csv = 'Line: {0}\n\n'.format(table_id)

    #pprint(table_result['Text'])
    csv = table_result['Text']

    return csv

def main(args):

    input_loc = args[1]
    output_loc = args[2]

    if (input_loc[len(input_loc)-1] == '/'):
        input_loc = input_loc[:-1]

    if (output_loc[len(output_loc)-1] == '/'):
        output_loc = output_loc[:-1]

    input_url = urlparse(input_loc)
    output_url = urlparse(output_loc)

    bucket = input_url.netloc
    key = input_url.path[1:]

    print(key)

    s3 = boto3.client('s3')
    response = s3.list_objects(Bucket=bucket, Prefix=key)

    for content in response['Contents']:
        if (content['Size'] > 0):
            print(content['Key'])
            file_name = content['Key']
            csv_content = get_table_csv_results(bucket,file_name)

            csv_file = os.path.basename(file_name)
            output_file = '{}.csv'.format(csv_file)

            # replace content
            body = bytes(csv_content)
            resp = s3.put_object(Bucket=output_url.netloc,
                                 Key="{}/{}".format(output_url.path[1:],output_file),
                                 Body=body)
            time.sleep(5)


if __name__ == "__main__":
    main(sys.argv)