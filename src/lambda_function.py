import boto3
import json

# Bedrock runtime client
bedrock = boto3.client('bedrock-runtime', region_name='us-east-2')

# inference profile ARN for Claude 3.7 Sonnet
model_id = 'INSERT ARN HERE'            # removed for security reasons (public repo)

def lambda_handler(event, context):
    print('Event:', json.dumps(event))

    # 1) Parse the incoming prompt
    request_body = json.loads(event.get('body', '{}'))
    prompt = request_body.get('prompt', '')

    # 2) Build the Messages API payload
    payload = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 400,
        "temperature": 0.75,
        "messages": [
            { "role": "user", "content": prompt }
        ]
    }

    try:
        # 3) Invoke using the inference-profile ARN
        resp = bedrock.invoke_model(
            modelId=model_id,
            body=json.dumps(payload),
            contentType='application/json',
            accept='application/json'
        )
        response_body = json.loads(resp['body'].read())
        print('Bedrock response:', json.dumps(response_body))

        # 4) Extract the assistant’s text from the Messages API response
        response_text = ''
        if response_body.get('type') == 'message' and response_body.get('role') == 'assistant':
            for block in response_body.get('content', []):
                if block.get('type') == 'text':
                    response_text = block.get('text', '')
                    break

    except Exception as e:
        print('InvokeModel error:', str(e))
        raise  # ensure API Gateway surfaces a 502 on failure

    # 5) Return the prompt + Claude reply
    return {
        'statusCode': 200,
        'body': json.dumps({
            'prompt':  prompt,
            'response': response_text
        })
    }