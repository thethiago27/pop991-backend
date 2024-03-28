import json

import boto3


def lambda_handler(event, context):
    invoice_id = event.get('invoice_id')

    invoice = get_invoice(invoice_id)
    status = invoice.get('status')

    if status != 'pending':
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Invoice already processed"})
        }

    user_id = invoice.get('user_id')
    amount = invoice.get('amount')

    deposit_balance(user_id, amount)
    update_invoice_status(invoice_id)

    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Balance updated successfully"})
    }


def deposit_balance(user_id, amount):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('balance')
    response = table.update_item(
        Key={
            'user_id': user_id
        },
        UpdateExpression='SET balance = balance + :val',
        ExpressionAttributeValues={
            ':val': amount
        }
    )
    return response['Attributes']


def update_invoice_status(invoice_id):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('invoices')
    response = table.update_item(
        Key={
            'invoice_id': invoice_id
        },
        UpdateExpression='SET #status = :status',
        ExpressionAttributeNames={'#status': 'status'},
        ExpressionAttributeValues={':status': 'finished'}
    )
    return response['Attributes']


def get_invoice(invoice_id):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('invoices')
    response = table.get_item(
        Key={
            'invoice_id': invoice_id
        }
    )
    return response['Item']
