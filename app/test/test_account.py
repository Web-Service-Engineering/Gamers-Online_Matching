import json

#from app.main.service.account_service import encode_auth_token, decode_auth_token
from app.test.base import BaseTestCase


def mocking_get_response(self, is_empty, is_get_all):
    if is_empty:
        _response = json.dumps({"data": []})
    else:
        _response = json.dumps({'data': [{'email': 'test@email.com',
                                          'password': '123456',
                                          'id': '4'}]})

    if is_get_all:
        _status = 200
    else:
        _status = 404

    mocking_response = self.app.response_class(
        response=_response,
        status=_status,
        mimetype='application/json'
    )
    return mocking_response


def mocking_post_response(self, status):
    if status == 'success':
        _response = json.dumps({'status': 'success',
                                'message': 'Successfully registered.'})
        _status = 201
    else:
        _response = json.dumps({'status': 'fail',
                                'message': 'Account already exists. Please Log in.'})
        _status = 409

    mocking_response = self.app.response_class(
        response=_response,
        status=_status,
        mimetype='application/json'
    )
    return mocking_response


class TestAccount(BaseTestCase):
    def test_list_accounts_controller(self):
        expected_output = mocking_get_response(self, False, True)
        self.mock_get_list_controller.return_value = expected_output
        expected_output_dict = json.loads(expected_output.data.decode('utf-8'))
        user_response = self.client.get('/account/')

        content_type = user_response.content_type

        self.assertIn('application/json', content_type)
        self.assert200(user_response)
        self.assertEqual(user_response.json, expected_output_dict)
        self.assertEqual(len(user_response.json['data']), 1)
        self.mock_get_list_controller.assert_called_once()

    def test_list_accounts_controller_empty(self):
        expected_output = mocking_get_response(self, True, True)
        self.mock_get_list_controller.return_value = expected_output
        expected_output_dict = json.loads(expected_output.data.decode('utf-8'))

        user_response = self.client.get('/account/')
        content_type = user_response.content_type

        self.assertIn('application/json', content_type)
        self.assert200(user_response)
        self.assertEqual(user_response.json, expected_output_dict)
        self.assertEqual(len(user_response.json['data']), 0)
        self.mock_get_list_controller.assert_called_once()

    def test_get_account_by_id_controller(self):
        expected_output = mocking_get_response(self, False, True)
        self.mock_get_list_controller.return_value = expected_output
        expected_output_dict = json.loads(expected_output.data.decode('utf-8'))

        user_response = self.client.get('/account/4')
        content_type = user_response.content_type

        self.assertIn('application/json', content_type)
        self.assert200(user_response)
        self.assertEqual(user_response.json, expected_output_dict)
        self.assertEqual(len(user_response.json['data']), 1)

        expected_output = mocking_get_response(self, False, False)
        self.mock_get_list_controller.return_value = expected_output
        user_response = self.client.get('/account/4')
        self.assertEqual(user_response.status_code, 404)

        self.assertEqual(len(self.mock_get_list_controller.mock_calls), 2)

    def test_get_account_by_email_controller(self):
        expected_output = mocking_get_response(self, False, True)
        self.mock_get_list_controller.return_value = expected_output
        expected_output_dict = json.loads(expected_output.data.decode('utf-8'))

        user_response = self.client.get('/account/test@email.com')
        content_type = user_response.content_type

        self.assertIn('application/json', content_type)
        self.assert200(user_response)
        self.assertEqual(user_response.json, expected_output_dict)
        self.assertEqual(len(user_response.json['data']), 1)

        expected_output = mocking_get_response(self, False, False)
        self.mock_get_list_controller.return_value = expected_output
        user_response = self.client.get('/account/test@email.com')
        self.assertEqual(user_response.status_code, 404)

        self.assertEqual(len(self.mock_get_list_controller.mock_calls), 2)

    def test_register_account_controller_success(self):
        expected_output = mocking_post_response(self, 'success')
        self.mock_save_controller.return_value = expected_output
        expected_output_dict = json.loads(expected_output.data.decode('utf-8'))

        payload = {'email': 'test@email.com',
                   'password': '123456',
                   'id': '4'}
        user_response = self.client.post('/account/', json=payload)
        content_type = user_response.content_type

        self.assertIn('application/json', content_type)
        self.assertEqual(expected_output_dict['status'], 'success')
        self.assertEqual(user_response.status_code, 201)
        self.assertEqual(user_response, expected_output)
        self.mock_save_controller.assert_called_once()

    def test_register_account_controller_fail(self):
        expected_output = mocking_post_response(self, 'fail')
        self.mock_save_controller.return_value = expected_output
        expected_output_dict = json.loads(expected_output.data.decode('utf-8'))

        payload = {'email': 'test@email.com',
                   'password': '123456',
                   'id': '4'}
        user_response = self.client.post('/account/', json=payload)
        content_type = user_response.content_type

        self.assertIn('application/json', content_type)
        self.assertEqual(expected_output_dict['status'], 'fail')
        self.assertEqual(user_response.status_code, 409)
        self.assertEqual(user_response, expected_output)
        self.mock_save_controller.assert_called_once()

    # def test_encode_token(self):
    #     auth_token = encode_auth_token(self, 4)
    #     self.assertTrue(isinstance(auth_token, str))
    #
    # def test_decode_token(self):
    #     auth_token = encode_auth_token(self, 4)
    #     self.assertTrue(isinstance(auth_token, str))
    #     self.assertTrue(decode_auth_token(auth_token), str)
