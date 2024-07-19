# CCLDevOpsTask

## Solution-1: Cognito User Pool Deployment

### Steps to Deploy the Solution:

1. **Clone the Repository:**
   - Access the Solution-2 directory by navigating to `/CCLDevOpsTask/Solution-1-Cognito`.
   - Clone the repository to your local machine by running the following command:
     ```bash
     git clone https://github.com/sajidrai/CCLDevOpsTask.git
     cd CCLDevOpsTask/Solution-1-Cognito
     ```
2. **Run Applicaiton Locally:**
   - Navigating to following folder `CCLDevOpsTask/Solution-1-Cognito/BasicApp`.
   - Run local application by running the following command:
     ```bash
     python -m http.server 3000
     ```
3. **Deploy Cognito User Pool using CloudFormation:**
   - Access the `cognito-final.yaml` file located in `CCLDevOpsTask/Solution-1-Cognito`.
   - Go to the AWS Management Console and navigate to the CloudFormation service.
   - Click on "Create stack" and choose "With new resources (standard)".
   - Upload the `cognito-final.yaml` CloudFormation template.
   - Proceed with the stack creation by following the on-screen instructions.
   - Once the stack creation is complete, the Cognito User Pool, User Pool Client, and related resources will be deployed.

4. **Testing:**
   - after successful creation of the stack In the outputs we have `SignInURL, LogoutURL, SignUpURL` .
   - We can perform any operation sing in, signout and signup using mentioned links.

### Note:
- Ensure that the necessary parameters in the CloudFormation template are correctly set before deploying the stack.
- Make sure you have the required permissions and AWS credentials to create resources using CloudFormation.
- Replace placeholders like `<CognitoDomain>`, `<AWS::Region>`, `<UserPoolClient>`, and URLs with actual values as needed.

Follow these steps to deploy and configure the Cognito User Pool using AWS CloudFormation and set up the Hosted UI for user authentication.

## Solution-2: ApiGateway-Lambda-DynamoDB-SES

### Steps to Deploy the Solution:

1. **Clone the Repository:**
   - Access the Solution-2 directory by navigating to `/CCLDevOpsTask/Solution-2-ApiGateway-Lambda-dynamodb-SES`.
   - Clone the repository to your local machine by running the following command:
     ```bash
     git clone https://github.com/sajidrai/CCLDevOpsTask.git
     cd CCLDevOpsTask/Solution-2-ApiGateway-Lambda-dynamodb-SES
     ```

2. **Upload Lambda Function ZIPs to S3:**
   - Run the `upload_files_to_s3.sh` script to upload the Lambda function ZIPs and JWT Python library ZIP to the S3 bucket. This script will create the necessary ZIP files and upload them to the specified S3 bucket, make sure to update your secret key, private key and region in the file before running this script.
     ```bash
     ./upload_files_to_s3.sh
     ```

3. **Deploy Infrastructure using AWS Console:**
   - Go to the AWS Management Console and navigate to the CloudFormation service.
   - Click on "Create stack" and choose "With new resources (standard)".
   - Upload the `apiGatewayLambdaDynamodbSESSolution.yaml` CloudFormation template.
   - Fill in the necessary parameters like Region, AccountId, EnvironmentName, UserTokensTableName, SenderEmail, SecretKeyJwtToken, and S3BucketName.
   - Proceed with the stack creation by following the on-screen instructions.
   - Once the stack creation is complete, the infrastructure components including the DynamoDB table, Lambda functions, and API Gateway will be deployed.

3. **Testing**
   - Once the stack is completed we can copy the `To` and call it using postman by providing json object in the body as 
   `{"email": "emailAddress}`.
   - Above will send token to email as well as in api response for testing purpose.
   - To verify token we can call `tokenVerfication` api by copying its link from the outputs with key as `` and provide a verification code in the body as `{"verification_code": "code"}`
   - This verify the token or gave error based on the token value.

### Note:
- Ensure that the sender email address and the recipient email address for verification code emails are verified in the Amazon SES console under the "Email Addresses" section.
- Make sure you have the necessary AWS credentials configured on your local machine before running the scripts and CloudFormation commands.
- Replace placeholders like `<repository_url>`, `<stack_name>`, `<region>`, `<account_id>`, `<environment>`, `<table_name>`, `<sender_email>`, `<jwt_secret>`, and `<s3_bucket_name>` with your actual values.

Follow these steps to deploy Solution-2 using AWS CloudFormation and effectively manage the Lambda functions, DynamoDB table, and SES integration.
