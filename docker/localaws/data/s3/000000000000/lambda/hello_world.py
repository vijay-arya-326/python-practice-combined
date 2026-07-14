import json


def lambda_handler(event, context):
    # Log the incoming event to CloudWatch (helpful for debugging)
    print(f"Received event: {json.dumps(event)}")

    # Extract a name from the event if it exists, otherwise default to "World"
    name = event.get('name', 'World')

    # Return a standard API Gateway compatible response
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps({
            'message': f'Hello, {name}!'
        })
    }


if __name__ == '__main__':
    fake_custom_event = {
        "user_id": "usr_98765",
        "action": "update_profile",
        "payload": {
            "email": "testuser@example.com",
            "theme": "dark"
        },
        "request_timestamp": 1783422120
    }
    a = lambda_handler(fake_custom_event, "Vijay")
    print(a)