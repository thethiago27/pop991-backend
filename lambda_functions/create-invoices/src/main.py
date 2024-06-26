import json
import os
from datetime import datetime, timedelta
import boto3
import requests


def lambda_handler(event, context):
    content = json.loads(event['body'])
    amount = content.get('amount')
    user_id = event.get('principalId')

    qr_code_id, qr_code_payload = create_pix_code(amount)
    save_invoice(amount, qr_code_id, qr_code_payload, user_id)
    notify_transaction(amount, user_id)

    return {
        'statusCode': 200,
        'body': json.dumps({
            'qr_code_id': qr_code_id,
            'qr_code_payload': qr_code_payload
        })
    }


def save_invoice(amount, qr_code_id, qr_code_payload, user_id):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('invoices')

    item = {
        'invoice_id': qr_code_id,
        'user_id': user_id,
        'amount': amount,
        'qr_code_id': qr_code_id,
        'qr_code_payload': qr_code_payload,
        'status': 'pending',
        'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    table.put_item(Item=item)


def notify_transaction(amount, user_id):
    sns = boto3.client('sqs')

    content = json.dumps({
        'amount': amount,
        'user_id': user_id,
        'type': 'deposit'
    })

    sns.send_message(
        QueueUrl=os.getenv('transaction_queue_url'),
        MessageBody=content
    )


def create_pix_code(amount):
    url = "https://api.asaas.com/v3/pix/qrCodes/static"
    headers = {
        "Content-Type": "application/json",
        "access_token": os.getenv('asaas_token')
    }

    expiration_date = datetime.now() + timedelta(minutes=10)
    expiration_date_str = expiration_date.strftime("%Y-%m-%d %H:%M:%S")

    data = {
        "addressKey": os.getenv('pix_key'),
        "description": "Recarga de saldo",
        "value": amount,
        "format": "PAYLOAD",
        "expirationDate": expiration_date_str
    }

    response = requests.post(url, headers=headers, json=data)

    response_json = response.json()

    qr_code_id = response_json.get('id')
    qr_code_payload = response_json.get('payload')

    return qr_code_id, qr_code_payload
