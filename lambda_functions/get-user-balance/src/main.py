import boto3


def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    user_id = context['authorizer']['user_id']
    table = dynamodb.Table('balance')
    response = table.get_item(Key={'user_id': user_id})
    item = response.get('Item')
    if item:
        return {'balance': item.get('balance')}
    else:
        return None
