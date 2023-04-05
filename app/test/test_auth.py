import json
from app.test.base import BaseTestCase

payload = {
    "email": "test@testemail.com",
    "password": "\x2432622431302457702f424a2f68737763484b586"
}


def mocking_response_login(self, type):
    if type == "login_success":
        _response = json.dumps({
            'status': 'success',
            'message': 'Successfully logged in.',
            'Authorization': "6d6e33376a353839585968456d6e326b4775324535504e4b684569437065472f654e346971714a597636456f744757432e"
        })
        _status = 200
    elif type == "login_fail":
        _response = json.dumps({
            'status': 'fail',
            'message': 'Email or password does not match.',
        })
        _status = 401
    elif type == "login_exception":
        e = Exception("Try again.")
        _response = json.dumps({
            'status': 'fail',
            'message': str(e),
        })
        _status = 401

    mocking_response = self.app.response_class(
        response=_response,
        status=_status,
        mimetype='application/json'
    )
    return mocking_response


def mocking_response_logout(self, type):
    if type == "logout_invalid_auth_not_string":
        _response = json.dumps({
            'status': 'fail',
            'message': "Invalid Token not a String"
        })
        _status = 401
    elif type == "logout_invalid_auth":
        _response = json.dumps({
            'status': 'fail',
            'message': 'Provide a valid auth token.'
        })
        _status = 403

    mocking_response = self.app.response_class(
        response=_response,
        status=_status,
        mimetype='application/json'
    )
    return mocking_response


def mocking_response_get_logged_in_account(self, type):
    if type == "get_logged_in_success":
        _response = json.dumps({
            'status': 'success',
            'data': {
                'account_id': 1,
                'email': "test@testemail.com"
            }
        })
        _status = 200
    elif type == "get_logged_in_fail":
        _response = json.dumps({
            'status': 'fail',
            'message': 'Invalid Token not a String',
        })
        _status = 401
    elif type == "get_logged_in_invalid_auth":
        _response = json.dumps({
            'status': 'fail',
            'message': 'Provide a valid auth token.'
        })
        _status = 401

    mocking_response = self.app.response_class(
        response=_response,
        status=_status,
        mimetype='application/json'
    )
    return mocking_response


class TestAuth(BaseTestCase):

    def test_login_controller_success(self):
        expected_output = mocking_response_login(self, "login_success")
        self.mock_save_controller.return_value = expected_output
        expected_output_dict = json.loads(expected_output.data.decode('utf-8'))

        user_response = self.client.post('/authenticate/login', json=payload)
        content_type = user_response.content_type

        self.assertIn('application/json', content_type)
        self.assertEqual(expected_output_dict['status'], 'success')
        self.assertEqual(expected_output_dict['message'], 'Successfully logged in.')
        self.assertEqual(expected_output_dict['Authorization'], '6d6e33376a353839585968456d6e326b4775324535504e4b684569437065472f654e346971714a597636456f744757432e')
        self.assert200(user_response)
        self.assertEqual(user_response, expected_output)
        self.assertEqual(len(self.mock_save_controller.mock_calls), 1)

    def test_login_controller_fail(self):
        expected_output = mocking_response_login(self, "login_fail")
        self.mock_save_controller.return_value = expected_output
        expected_output_dict = json.loads(expected_output.data.decode('utf-8'))

        user_response = self.client.post('/authenticate/login', json=payload)
        content_type = user_response.content_type

        self.assertIn('application/json', content_type)
        self.assertEqual(expected_output_dict['status'], 'fail')
        self.assertEqual(expected_output_dict['message'], 'Email or password does not match.')
        self.assert401(user_response)
        self.assertEqual(user_response, expected_output)
        self.assertEqual(len(self.mock_save_controller.mock_calls), 1)

    def test_login_controller_exception(self):
        expected_output = mocking_response_login(self, "login_exception")
        self.mock_save_controller.return_value = expected_output
        expected_output_dict = json.loads(expected_output.data.decode('utf-8'))

        user_response = self.client.post('/authenticate/login', json=payload)
        content_type = user_response.content_type

        self.assertIn('application/json', content_type)
        self.assertEqual(expected_output_dict['status'], 'fail')
        self.assertEqual(expected_output_dict['message'], 'Try again.')
        self.assert401(user_response)
        self.assertEqual(user_response, expected_output)
        self.assertEqual(len(self.mock_save_controller.mock_calls), 1)
