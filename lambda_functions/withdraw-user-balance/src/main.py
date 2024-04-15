import logging
import os

import boto3

logger = logging.getLogger()
dynamodb = boto3.resource('dynamodb')
balance_table = dynamodb.Table('balance')


def lambda_handler(event, context):
    amount = event["Records"][0]["Sns"]["MessageAttributes"]["amount"]["Value"]
    user_id = event["Records"][0]["Sns"]["MessageAttributes"]["user_id"]["Value"]

    get_user_balance(user_id, amount)

    return {
        "statusCode": 200,
        "body": "Balance updated successfully",
    }


def notify_transaction(amount, user_id):
    sns = boto3.client('sns')
    sns.publish(
        TopicArn=os.getenv('sns_transaction_topic_arn'),
        MessageAttributes={
            'amount': {
                'DataType': 'String',
                'StringValue': amount
            },
            'user_id': {
                'DataType': 'String',
                'StringValue': user_id
            },
            'type': {
                'DataType': 'String',
                'StringValue': 'withdraw'
            }
        },
        Message="Transaction registered successfully"
    )


def get_user_balance(user_id, amount):
    logger.info(f"Withdraw {amount} to user {user_id}")
    balance_table.update_item(
        Key={'user_id': user_id},
        UpdateExpression='SET balance = balance - :val',
        ExpressionAttributeValues={':val': amount}
    )
    logger.info("Balance updated successfully")
