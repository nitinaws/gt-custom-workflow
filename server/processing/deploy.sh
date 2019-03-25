#!/bin/sh

if [ $# != 1 ]
then
  echo "Usage deploy.sh <s3 bucket name>"
  exit -1
fi

if [ -f 'labeling_lambda.zip' ] 
then   
  echo True
fi

zip labeling_lambda.zip *.py

aws s3 cp labeling_lambda.zip s3://$1/coderepo/

aws s3 cp cfn-template.json s3://$1/cft/

rm labeling_lambda.zip
