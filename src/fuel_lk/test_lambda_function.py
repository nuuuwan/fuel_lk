
import json
import unittest

from lambda_function import encode, lambda_handler


def lambda_handler_wrapper(event, context):
    response = lambda_handler(event, context)
    return json.loads(response['body'])


def lambda_handler_wrapper_with_params(params):
    event = {
        'queryStringParameters': params,
    }
    context = None
    return lambda_handler_wrapper(event, context)


def lambda_handler_wrapper_with_payload(payload):
    params = {
        'payload_json_base64': encode(payload),
    }
    return lambda_handler_wrapper_with_params(params)


class TestCase(unittest.TestCase):
    def testMissingEvent(self):
        self.assertEqual(
            {'exception': 'Missing event'},
            lambda_handler_wrapper(None, None),
        )

    def testMissingCmd(self):
        self.assertEqual(
            {'exception': 'Missing cmd'},
            lambda_handler_wrapper_with_payload(dict(
                dummy_param='dummy_param',
            )),
        )

    def testInvalidCmd(self):
        self.assertEqual(
            {'exception': 'Invalid cmd: dummy_cmd'},
            lambda_handler_wrapper_with_payload(dict(
                cmd='dummy_cmd',
            )),
        )

    def testCmdMultigetSheds(self):
        actual_shed_list = lambda_handler_wrapper_with_payload(
            dict(
                cmd='multiget_sheds',
                province=1,
                district=1,
                fuel_type='p92',
            )
        )
        self.assertTrue(
            len(actual_shed_list) > 0,
        )
        first_fuel_info = actual_shed_list[0]
        for k in [
            'shedId',
            'shedName',
            'lastupdatebyshed',
            'fuelType',
            'fuelCapacity',
            'bowserDispatch',
            'eta',
            'shedownerupdatetoday',
        ]:
            self.assertIn(
                k,
                first_fuel_info,
            )

    def testCmdGetShed(self):
        actual_shed = lambda_handler_wrapper_with_payload(
            dict(
                cmd='get_shed',
                shed_id=10,
            )
        )
        for k in [
            'shedName',
            'shedCode',
            'address',
            'latitude',
            'longitude',
        ]:
            self.assertIn(
                k,
                actual_shed,
            )
