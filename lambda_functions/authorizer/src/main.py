def lambda_handler(event, context):
    response = {
        "isAuthorized": False,
        "context": {
            "stringKey": "value",
            "numberKey": 1,
            "booleanKey": True,
        }
    }

    try:
        token = event['headers']['Authorization']

        if not token:
            return response

        if token == 'Bearer token':
            response = {
                "isAuthorized": True,
                "context": {
                    "stringKey": "value",
                    "numberKey": 1,
                    "booleanKey": True,
                    "arrayKey": ["user_id", "1234"],
                    "mapKey": {"user_id": "1234"}
                }
            }
        else:
            return response
    except BaseException:
        print("No token provided")
        return response
