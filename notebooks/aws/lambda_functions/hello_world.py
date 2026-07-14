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