from datetime import datetime
import uuid

import boto3

dynamodb = boto3.resource('dynamodb')


def lambda_handler(event, context):
    transaction_table = dynamodb.Table('transactions')

    for record in event['Records']:
        transaction = record['Sns']['MessageAttributes']
        transaction_table.put_item(Item={
            'transaction_id': str(uuid.uuid4()),
            'user_id': transaction['user_id']['Value'],
            'amount': transaction['amount']['Value'],
            'type': transaction['type']['Value'],
            'status': 'completed',
            'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    return {
        'statusCode': 201,
    }
