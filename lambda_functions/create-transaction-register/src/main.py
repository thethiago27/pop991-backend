import json
import os
from datetime import datetime
import uuid

import boto3

dynamodb = boto3.resource('dynamodb')
sqs = boto3.client('sqs')


def lambda_handler(event, context):
    transaction_table = dynamodb.Table('transactions')

    for record in event['Records']:
        transaction = json.loads(record['body'])
        receipt_handle = record['receiptHandle']
        transaction_table.put_item(Item={
            'transaction_id': str(uuid.uuid4()),
            'user_id': transaction['user_id'],
            'amount': transaction['amount'],
            'type': transaction['type'],
            'status': 'completed',
            'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        sqs.delete_message(
            QueueUrl=os.getenv('transaction_queue_url'),
            ReceiptHandle=receipt_handle
        )


