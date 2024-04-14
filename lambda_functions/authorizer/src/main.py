import logging
import os
import jwt

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    try:
        authorization_header = event.get('headers', {}).get('Authorization')

        if not authorization_header or not authorization_header.startswith('Bearer '):
            logger.info("Token não encontrado na solicitação")
            return generate_policy('user', 'Deny', event['methodArn'])

        token = authorization_header.split(' ')[1]

        try:
            is_authorized = jwt.decode(token, os.getenv('jwt_secret'), algorithms=['HS256'])

            if 'user_id' in is_authorized:
                return generate_policy(is_authorized['user_id'], 'Allow', event['methodArn'])
            else:
                logger.info("ID do usuário não encontrado no token")
                return generate_policy('user', 'Deny', event['methodArn'])

        except jwt.ExpiredSignatureError:
            logger.info("Token expirado")
            return generate_policy('user', 'Deny', event['methodArn'])

        except jwt.InvalidTokenError:
            logger.error("Token inválido")
            return generate_policy('user', 'Deny', event['methodArn'])

    except Exception as e:
        logger.error(f"Erro inesperado: {str(e)}")
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
