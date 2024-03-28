import json

import boto3


def lambda_handler(event, context):

    dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('log')
    table.put_item(Item={
        'event': event,
        'context': context,
        'event_id': 'get-user-balance-2'
    })

    principal_id = event.get('requestContext').get('authorizer').get('principalId')
    table = dynamodb.Table('balance')
    response = table.get_item(Key={'user_id': principal_id})
    item = response.get('Item')
    if item:
        return {'balance': item.get('balance')}
    else:
        return {
            'statusCode': 404,
            'body': json.dumps({'message': 'User not found', event: event})
        }