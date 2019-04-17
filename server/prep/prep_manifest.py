import sys
import boto3
import json
from urllib.parse import urlparse
from faker import Faker

faker = Faker()

def prepare(s3_image_path,s3_data_path ,s3_manifest_path):

    image_url = urlparse(s3_image_path)
    data_url = urlparse(s3_data_path)
    output_url = urlparse(s3_manifest_path)


    s3 = boto3.client("s3")

    image_response = s3.list_objects(Bucket=image_url.netloc, Prefix=image_url.path[1:])
    text_response = s3.list_objects(Bucket=data_url.netloc,Prefix=data_url.path[1:] )

    image_list = parse_response(image_response)
    text_file_list = parse_response(text_response)

    content_list = []

    for item in image_list:
        print(item)
        image_filename = item.split('/')[-1]
        text_filename = "{}.csv".format(image_filename)
        print ("Trying to find {}/{}".format(data_url.path[1:] ,text_filename))
        entry = {}
        if "{}/{}".format(data_url.path[1:],text_filename) in text_file_list:
            print("Adding new Entry")
            entry['source-ref'] = "s3://{}/{}".format(image_url.netloc,item)
            entry['text-file-s3-uri'] = "s3://{}/{}/{}".format(data_url.netloc,data_url.path[1:],text_filename)
            entry['metadata'] = fake_metadata()
            print(entry)
            content_list.append(entry)

    print(content_list)
    content = "".join(str("{}\n".format(line)) for line in content_list)


    body = bytes(content,'utf-8')

    resp = s3.put_object(Bucket=output_url.netloc, Key="{}/manifest.json".format(output_url.path[1:]), Body=body)


def parse_response(response):
    list=[]
    prefix = ''
    for content in response['Contents']:
        if (content['Size'] > 0):
            print(content['Key'])
            file_name = content['Key']
            list.append(file_name)

    return list

def fake_metadata():

    return { "Author": faker.name(), "ISBN": faker.isbn10() };


def main(args):
   try:
        s3_image_path = args[1]
        s3_data_path = args[2]
        s3_manifest_path = args[3]

        prepare(s3_image_path,s3_data_path,s3_manifest_path)

   except:
       raise

if __name__ == "__main__":

    main(sys.argv)
