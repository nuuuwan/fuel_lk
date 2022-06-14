import base64
import json
import ssl
import urllib.request

ssl._create_default_https_context = ssl._create_unverified_context


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


def generic_post_request(url, request_data):
    req = urllib.request.Request(url)
    req.add_header(
        'Content-Type',
        'application/json; charset=utf-8',
    )
    request_data_json = json.dumps(request_data)
    request_data_json_bytes = request_data_json.encode('utf-8')
    req.add_header('Content-Length', len(request_data_json_bytes))
    response = urllib.request.urlopen(req, request_data_json_bytes)

    response_data_json = response.read()
    response_data = json.loads(response_data_json)
    return response_data


def multiget_sheds(province, district, fuel_type):
    url = 'https://fuel.gov.lk/api/v1/sheddetails/search'
    request_data = dict(
        province=province, district=district, fuelType=fuel_type,
    )
    return generic_post_request(url, request_data)


def run_payload(payload):
    cmd = payload.get('cmd', None)
    if not cmd:
        raise Exception('Missing cmd')

    body = None
    if cmd == 'multiget_sheds':
        if 'province' not in payload:
            raise Exception('Missing param: province')
        if 'district' not in payload:
            raise Exception('Missing param: district')
        if 'fuel_type' not in payload:
            raise Exception('Missing param: fuel_type')

        body = multiget_sheds(
            payload['province'],
            payload['district'],
            payload['fuel_type'],
        )
    else:
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
