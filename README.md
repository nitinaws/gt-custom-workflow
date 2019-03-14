## Build your own custom labeling workflow using SageMaker Ground Truth

Successful machine learning models are built on the shoulders of large volumes of high-quality training data. But, the process to create the training data necessary to build these models is often expensive, complicated, and time-consuming. The majority of models created today require a human to manually label data in a way that allows the model to learn how to make correct decisions.
Amazon SageMaker Ground Truth significantly reduces the time and effort required to create datasets for training to reduce costs. These savings are achieved by using machine learning to automatically label data. The model is able to get progressively better over time by continuously learning from labels created by human labelers.
Amazon SageMaker Ground Truth provides commonly used task HTML templates and workflows to solve many Vision, NLP and other use cases. It also provides enhanced HTML elements that makes building custom template easier and provide a familiar UI to workers. However, customers may need to build custom workflow for various reasons such as,

  - Branded styling and user experience consistent with IT policies
  - Complex input consisting of multiple elements per task as images, text, custom metadata
  - Dynamic decision making on task input to prevent certain item from going to worker
  - Consolidating labelling output for subsequent training job

In this blog post, we demonstrate a custom text annotation labeling workflow to build labelled dataset for Natural language processing (NLP) problem


#### Augumented Manifest
server/data/manifest.json
server/data/mini_manifest.json

#### Script to extract text using Amazon Textract
server/prep/detect_lines.py

#### Script to create Manifest
server/prep/prep_manifest.py

#### Cloudformation script to deploy Lambda
server/processing/cfn-template.json
server/processing/labeling_lambda.zip

#### Pre and post labeling lambdas
server/processing/sagemaker-gt-postprocess.py
server/processing/sagemaker-gt-preprocess.py

#### React Components
web/README.md
web/package.json
web/src/App.css
web/src/App.js
web/src/App.test.js
web/src/index.css
web/src/index.js
web/public/index.html
web/public/manifest.json
web/public/template.html
