import logging
import os
import jwt

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    authorization_header = event['headers']['Authorization']
    token = None

    if authorization_header.startswith('Bearer '):
        logger.info("Error no auth")
        token = authorization_header.split(' ')[1]

    if not token:
        logger.info("Token n encontrado")
        return generate_policy('user', 'Deny', event['methodArn'])

    try:
        is_authorized = jwt.decode(token, os.getenv('jwt_secret'), algorithms=['HS256'])

        if 'user_id' in is_authorized:
            return generate_policy(is_authorized['user_id'], 'Allow', event['methodArn'])
        else:
            return generate_policy('user', 'Deny', event['methodArn'])

    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return generate_policy('user', 'Deny', event['methodArn'])


def generate_policy(principal_id, effect, method_arn):
    policy = {
        'principalId': principal_id,
        'policyDocument': {
            'Version': '2012-10-17',
            'Statement': [{
                'Action': 'execute-api:Invoke',
                'Effect': effect,
                'Resource': method_arn
            }]
        }
    }

    return policy
