import json
import jwt
import boto3
import time
from decimal import Decimal
from boto3.dynamodb.types import TypeDeserializer
import os

dynamodb = boto3.resource('dynamodb')

DYNAMODB_TABLE_NAME = os.environ.get('UserTokensTableName')
SECRET_KEY = os.environ.get('SecretKeyJwtToken')

table = dynamodb.Table(DYNAMODB_TABLE_NAME)
deserializer = TypeDeserializer()

def get_verification_code_item(verification_code):
    response = table.scan(
        FilterExpression='verification_code = :vc',
        ExpressionAttributeValues={':vc': verification_code}
    )
    return response['Items'][0] if response['Items'] else None

def deserialize_item(item):
    email = item['email']
    token = item['token']
    expiration_time = deserializer.deserialize({'N': str(item['expiration_time'])})
    return email, token, expiration_time

def decode_token(token):
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return decoded_token['email'], None
    except jwt.ExpiredSignatureError:
        return None, 'Token has expired'
    except jwt.InvalidTokenError:
        return None, 'Invalid token'

def verify_token_email(token_email, item_email):
    return token_email == item_email

def is_token_expired(expiration_time):
    return int(time.time()) > expiration_time

def response(status_code, message):
    return {
        'statusCode': status_code,
        'body': json.dumps(message)
    }

def lambda_handler(event, context):
    body = json.loads(event['body'])
    verification_code = int(body['verification_code'])

    item = get_verification_code_item(verification_code)
    if not item:
        return response(400, 'Invalid verification code')

    email, token, expiration_time = deserialize_item(item)
    token_email, error_message = decode_token(token)
    if error_message:
        return response(400, error_message)

    if not verify_token_email(token_email, email):
        return response(400, 'Email mismatch')

    if is_token_expired(expiration_time):
        return response(400, 'Token has expired')

    return response(200, {
        'email': email,
        'message': "Token verified successfully"
    })
