import json
from app.test.base import BaseTestCase

payload = {
    "account_id": 1,
    "responses": ["A", "S", "K", "E", "A", "S", "K", "E", "A", "S", "K", "E",
                  "A", "S", "K", "E", "A", "S", "K", "E", "A", "S", "K", "E",
                  "A", "S", "K", "E", "A", "S", "K", "E", "A", "S", "K"],
}


def mocking_response_save_bartle(self, type):
    if type == "save_success":
        _response = json.dumps({
            'status': 'success',
            'message': 'Successfully created.',
        })
        _status = 201
    elif type == "save_fail":
        _response = json.dumps({
            'status': 'fail',
            'message': 'Failed to store bartle test results.',
        })
        _status = 500
    elif type == "update_success":
        _response = json.dumps({
            'status': 'success',
            'message': 'Successfully updated.',
        })
        _status = 201

    mocking_response = self.app.response_class(
        response=_response,
        status=_status,
        mimetype='application/json'
    )
    return mocking_response


class TestBartlequotient(BaseTestCase):

    def test_save_new_bartle_controller_success(self):
        expected_output = mocking_response_save_bartle(self, "save_success")
        self.mock_save_controller.return_value = expected_output
        expected_output_dict = json.loads(expected_output.data.decode('utf-8'))

        user_response = self.client.post('/bartlequotient/', json=payload)
        content_type = user_response.content_type

        self.assertIn('application/json', content_type)
        self.assertEqual(expected_output_dict['status'], 'success')
        self.assertEqual(expected_output_dict['message'], 'Successfully created.')
        self.assertEqual(user_response.status_code, 201)
        self.assertEqual(user_response, expected_output)
        self.assertEqual(len(self.mock_save_controller.mock_calls), 1)

    def test_save_new_bartle_controller_fail(self):
        expected_output = mocking_response_save_bartle(self, "save_fail")
        self.mock_save_controller.return_value = expected_output
        expected_output_dict = json.loads(expected_output.data.decode('utf-8'))

        user_response = self.client.post('/bartlequotient/', json=payload)
        content_type = user_response.content_type

        self.assertIn('application/json', content_type)
        self.assertEqual(expected_output_dict['status'], 'fail')
        self.assertEqual(expected_output_dict['message'], 'Failed to store bartle test results.')
        self.assert500(user_response)
        self.assertEqual(user_response, expected_output)
        self.assertEqual(len(self.mock_save_controller.mock_calls), 1)

    def test_update_new_bartle_controller_success(self):
        expected_output = mocking_response_save_bartle(self, "update_success")
        self.mock_save_controller.return_value = expected_output
        expected_output_dict = json.loads(expected_output.data.decode('utf-8'))

        user_response = self.client.post('/bartlequotient/', json=payload)
        content_type = user_response.content_type

        self.assertIn('application/json', content_type)
        self.assertEqual(expected_output_dict['status'], 'success')
        self.assertEqual(expected_output_dict['message'], 'Successfully updated.')
        self.assertEqual(user_response.status_code, 201)
        self.assertEqual(user_response, expected_output)
        self.assertEqual(len(self.mock_save_controller.mock_calls), 1)
