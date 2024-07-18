import json
import boto3
import time
from datetime import datetime, timedelta
import random
import jwt
import os

# Import Cognito Identity Provider client
dynamodb = boto3.resource('dynamodb')

# Get environment variables  
SEND_VERIFICATION_CODE_LAMBDA_ARN = os.environ.get('SendVerificationCodeLambdaArn')  
DYNAMODB_TABLE_NAME = os.environ.get('UserTokensTableName') 
SENDER_EMAIL = os.environ.get('SenderEmail')
SECRET_KEY = os.environ.get('SecretKeyJwtToken')

# Create a Lambda client
lambda_client = boto3.client('lambda')

def invoke_email_lambda(sender_email, receiver_email, subject, body):
    payload = {
        'sender_email': sender_email,
        'receiver_email': receiver_email,
        'subject': subject,
        'body': body
    }

    response = lambda_client.invoke(
        FunctionName=SEND_VERIFICATION_CODE_LAMBDA_ARN,
        InvocationType='Event',  # Use 'RequestResponse' for synchronous execution, 'Event' for asynchronous
        Payload=json.dumps(payload)
    )

    return response

def lambda_handler(event, context):
    table = dynamodb.Table(DYNAMODB_TABLE_NAME)
    body = json.loads(event['body'])  
    
    # Access the 'email' attribute from the parsed data  
    email = body['email']

    token = jwt.encode({'email': email, 'exp': datetime.utcnow() + timedelta(minutes=30)}, SECRET_KEY, algorithm='HS256')
    verification_code = random.randint(10000, 999999)

    table.put_item(
        Item={
            'email': email,
            'token': token,
            'expiration_time': int(time.time()) + 1800,
            'verification_code': verification_code
        }
    )

    # Send email to the specified email address
    receiver_email = email
    email_subject = "Verification Code"
    email_body = f"Your verification code is: {verification_code}"

    response = invoke_email_lambda(SENDER_EMAIL, receiver_email, email_subject, email_body)

    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'Token created and saved in DynamoDB table "UserTokensTable"',
            'verification_code': verification_code
        })
    }
