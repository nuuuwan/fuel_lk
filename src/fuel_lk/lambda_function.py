import base64
import json


def decode(payload_json_base64):
    payload_json = base64.b64decode(payload_json_base64).decode()
    payload = json.loads(payload_json)
    return payload


def encode(payload):
    payload_json = json.dumps(payload)
    payload_json_base64 = base64.b64encode(payload_json.encode())
    return payload_json_base64


def get_payload(event, context):
    if not event:
        raise Exception('Missing event')

    params = event.get('queryStringParameters', {})
    if not params:
        raise Exception('Missing query params')

    payload_json_base64 = params.get('payload_json_base64', None)
    if not payload_json_base64:
        raise Exception('Missing payload_json_base64')

    payload = decode(payload_json_base64)
    return payload


def run_payload(payload):
    cmd = payload.get('cmd', None)
    body = None
    if not cmd:
        raise Exception('Missing cmd')

    if cmd == 'search':
        pass

    raise Exception(f'Invalid cmd: {cmd}')
    assert(body is not None)
    return body


def lambda_handler(event, context):
    try:
        payload = get_payload(event, context)
        body = run_payload(payload)
    except Exception as e:
        body = {'exception': str(e)}

    if 'exception' in body:
        print(body)

    return {
        'statusCode': 200,
        'body': json.dumps(body)
    }
