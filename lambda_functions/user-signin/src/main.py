import json
import os

import boto3
import jwt
from botocore.exceptions import ClientError


def lambda_handler(event, context):
    email = event['email']
    password = event['password']

    try:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('users_auth')
        response = table.get_item(Key={'email': email})

        if 'Item' not in response:
            return {
                'statusCode': 401,
                'body': json.dumps({
                    'message': 'User not found'
                })
            }

        user = response['Item']

        if user['password'] != password:
            return {
                'statusCode': 401,
                'body': json.dumps({
                    'message': 'Invalid password'
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
            })
        }

    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Erro ao acessar o DynamoDB: {}'.format(e.response['Error']['Message'])})
        }

