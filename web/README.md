#### Steps taken to create this project:
- Install Node, NPM Package Manager and Yarn(https://www.npmjs.com/package/yarn)

- Clone repository and install pre-requisites
    
    ```
    git clone https://github.com/nitinaws/gt-custom-workflow.git
    cd web
    yarn add react-text-annotate
    yarn build
    ```

- Update your s3 bucket/prefix in `package.json`  

   ```
   "clean": "aws s3 rm --recursive s3://<your s3 bucket>/web/",
   "deploy": "aws s3 cp --recursive build/ s3://<your s3 bucket>/web/ --acl public-read"
   ```

- Now run to upload project to S3 bucket
    ```yarn clean
       yarn deploy
    ```

- Make sure to change CSS and JS URLs to point to your S3 urls in `public\template.html`


