import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    """
    Simple HTTP Lambda handler that processes API Gateway events
    """
    logger.info(f"Received event: {json.dumps(event)}")
    
    # Extract HTTP method and path
    http_method = event.get('httpMethod', event.get('requestContext', {}).get('http', {}).get('method', 'UNKNOWN'))
    path = event.get('path', event.get('rawPath', '/'))
    
    # Extract query parameters
    query_params = event.get('queryStringParameters') or {}
    
    # Extract body if present
    body = event.get('body', '')
    
    # Process the request based on method
    if http_method == 'GET':
        response_body = {
            'message': 'Hello from AWS Lambda!',
            'path': path,
            'method': http_method,
            'queryParameters': query_params
        }
    elif http_method == 'POST':
        try:
            request_data = json.loads(body) if body else {}
            response_body = {
                'message': 'Data received successfully',
                'receivedData': request_data,
                'path': path
            }
        except json.JSONDecodeError:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({
                    'error': 'Invalid JSON in request body'
                })
            }
    else:
        response_body = {
            'message': f'Method {http_method} is supported',
            'path': path
        }
    
    # Return successful response
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type'
        },
        'body': json.dumps(response_body)
    }
