import os

import jwt


def lambda_handler(event, context):
    authorization_header = event['headers'].get('Authorization')

    try:
        if authorization_header and authorization_header.startswith('Bearer '):
            token = authorization_header.split(' ')[1]
            decoded_token = jwt.decode(token, os.getenv('jwt_secret'), algorithms=['HS256'])

            if 'username' in decoded_token:
                raise generate_policy(decoded_token['user_id'], 'Allow', event['methodArn'])
            else:
                raise generate_policy(decoded_token['user_id'], 'Deny', event['methodArn'])
    except jwt.ExpiredSignatureError:
        raise generate_policy("", 'Deny', event['methodArn'])
    except jwt.InvalidTokenError:
        raise generate_policy("", 'Deny', event['methodArn'])


def generate_policy(principal_id, effect, resource):
    return {
        'principalId': principal_id,
        'policyDocument': {
            'Version': '2012-10-17',
            'Statement': [{
                'Action': 'execute-api:Invoke',
                'Effect': effect,
                'Resource': resource
            }]
        }
    }
