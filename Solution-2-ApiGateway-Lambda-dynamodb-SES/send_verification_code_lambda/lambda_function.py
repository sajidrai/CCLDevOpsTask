import json
import boto3
import os

# Get environment variables  
REGION = os.environ.get('Region')

# Configure the Amazon SES client
ses_client = boto3.client('ses', region_name=REGION)  # Update the region as per your SES configuration

def send_email(sender_email, receiver_email, subject, body):
    response = ses_client.send_email(
        Destination={
            'ToAddresses': [receiver_email],
        },
        Message={
            'Body': {
                'Text': {
                    'Charset': 'UTF-8',
                    'Data': body,
                },
            },
            'Subject': {
                'Charset': 'UTF-8',
                'Data': subject,
            },
        },
        Source=sender_email
    )
    return response

def lambda_handler(event, context):
    print(f"in email sending lambda function")
    print(f"event : {event}")
    sender_email = event.get('sender_email')
    receiver_email = event.get('receiver_email')
    subject = event.get('subject')
    body = event.get('body')

    # Send email
    
    response = send_email(sender_email, receiver_email, subject, body)

    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'Email sent successfully.',
            'message_id': response['MessageId']
        })
    }
