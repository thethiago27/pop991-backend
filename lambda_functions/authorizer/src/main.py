import os
import jwt


def lambda_handler(event, context):
    authorization_header = event['headers'].get('authorization')

    response = {
        "isAuthorized": False,
        "context": {
            "stringKey": "value",
            "numberKey": 1,
            "booleanKey": True,
            "arrayKey": ["value1", "value2"],
            "mapKey": {"value1": "value2"}
        }
    }

    if not authorization_header:
        return response

    token = authorization_header.split(' ')[1]

    try:
        is_authorized = jwt.decode(token, os.getenv('jwt_secret'), algorithms=['HS256'])

        if 'user_id' in is_authorized:
            response['isAuthorized'] = True
            response['context']['user_id'] = is_authorized['user_id']
        else:
            response['isAuthorized'] = False
        return response

    except jwt.ExpiredSignatureError:
        is_authorized = False
        return response
    except jwt.InvalidTokenError:
        is_authorized = False
        return response

