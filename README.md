## Build your own custom labeling workflow using SageMaker Ground Truth

Successful machine learning models are built on the shoulders of large volumes of high-quality training data, but the process to create the training data necessary to build these models is expensive, complicated, and time-consuming. The majority of models created today require a human to manually label data in a way that allows the model to learn how to make correct decisions. 

Amazon SageMaker Ground Truth provides built-in workflows for image classification, bounding boxes, text classification, and semantic segmentation use cases. You also have the option of building your own custom workflows where you define the user interface (UI) for performing data labeling. To help you move quickly, SageMaker provides you a number of commonly used custom UI templates for image, text, and audio data labeling use cases. These templates take advantage of SageMaker Ground Truth’s crowd HTML elements that are meant to simplify the process of building data labeling UIs. You can also specify your own arbitrary HTML for the UI.

You may need to build custom workflow for various reasons, such as:
-	Your own custom data labeling requirements
-	Complex input consisting of multiple elements per task (e.g., images, text, or custom metadata)
-	Dynamic decision making on task input to prevent certain items from going to labelers
-	Custom logic for consolidating labeling output to improve labeling accuracy


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
web/publuc/test_template.html
