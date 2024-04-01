import json
import os

import boto3
import jwt
from botocore.exceptions import ClientError


def lambda_handler(event, context):
    event = json.loads(event['body'])

    try:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('users_auth')
        response = table.get_item(Key={'email': event['email']})

        if 'Item' not in response:
            return {
                'statusCode': 401,
                'body': json.dumps({
                    'message': 'Email or password invalid'
                })
            }

        user = response['Item']

        if user['password'] != event['password']:
            return {
                'statusCode': 401,
                'body': json.dumps({
                    'message': 'Email or password invalid'
                })
            }

        payload = {
            'user_id': user['user_id']
        }

        jwt_token = jwt.encode(payload, os.getenv('jwt_secret'), algorithm='HS256')

        return {
            'statusCode': 200,
            'body': json.dumps({
                'token': jwt_token
            }),
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Credentials': "true",
            }
        }

    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Erro ao acessar o DynamoDB: {}'.format(e.response['Error']['Message'])})
        }
