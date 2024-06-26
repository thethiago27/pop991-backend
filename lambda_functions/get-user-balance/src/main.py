import json
from decimal import Decimal

import boto3


def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')

    print(context)

    principal_id = event["principalId"]
    table = dynamodb.Table('balance')
    response = table.get_item(Key={'user_id': principal_id})
    item = response.get('Item')
    if item:
        return {
            'balance': float(item.get('balance')),
        }
    else:
        return {
            'statusCode': 404,
            'body': json.dumps({'message': 'User not found', 'event': event}),  # Fix the event representation
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Credentials': "true",
            }
        }

