import json

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
            'body': json.dumps({
                'balance': item.get('balance'),
            }),
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Credentials': "true",
            }
        }
    else:
        return {
            'statusCode': 404,
            'body': json.dumps({'message': 'User not found', event: event}),
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Credentials': "true",
            }
        }