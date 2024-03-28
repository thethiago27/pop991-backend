import json
import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')
balance_table = dynamodb.Table('balance')
invoices_table = dynamodb.Table('invoices')


def lambda_handler(event, context):
    try:
        invoice_id = event["Records"][0]["Sns"]["MessageAttributes"]["invoice_id"]["Value"]

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
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Internal Server Error"})
        }


def deposit_balance(user_id, amount):
    logger.info(f"Depositing {amount} to user {user_id}")
    balance_table.update_item(
        Key={'user_id': user_id},
        UpdateExpression='SET balance = balance + :val',
        ExpressionAttributeValues={':val': amount}
    )
    logger.info("Balance updated successfully")


def update_invoice_status(invoice_id):
    logger.info(f"Updating status of invoice {invoice_id}")
    invoices_table.update_item(
        Key={'invoice_id': invoice_id},
        UpdateExpression='SET #status = :status',
        ExpressionAttributeNames={'#status': 'status'},
        ExpressionAttributeValues={':status': 'finished'}
    )
    logger.info("Invoice status updated successfully")


def get_invoice(invoice_id):
    logger.info(f"Fetching invoice {invoice_id}")
    response = invoices_table.get_item(
        Key={'invoice_id': invoice_id}
    )
    return response.get('Item')
