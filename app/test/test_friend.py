import json
from app.test.base import BaseTestCase

payload = {
    "current_account_id": 1,
    "friend_account_id": 2,
}


def mocking_response_add_friend_exceptions(self, type):
    if type == "requestor_not_found":
        e = Exception('Current profile is not found')
    elif type == "requestor_equal_friend":
        e = Exception('You cannot friend yourself')
    elif type == "receiver_not_found":
        e = Exception('Friend''s account is not found')
    else:
        e = Exception('Already a friend')

    _response = json.dumps({
        'status': 'fail',
        'message': str(e)
    })
    _status = 404

    mocking_response = self.app.response_class(
        response=_response,
        status=_status,
        mimetype='application/json'
    )
    return mocking_response


def mocking_response_remove_friend_exceptions(self, type):
    if type == "requestor_not_found":
        e = Exception('Current profile is not found')
    elif type == "requestor_equal_friend":
        e = Exception('You cannot friend yourself')
    elif type == "receiver_not_found":
        e = Exception('Friend''s account is not found')

    _response = json.dumps({
        'status': 'fail',
        'message': str(e)
    })
    _status = 404

    mocking_response = self.app.response_class(
        response=_response,
        status=_status,
        mimetype='application/json'
    )
    return mocking_response


def mocking_response_add_friend_success(self):
    _response = json.dumps({
        'status': 'success',
        'message': 'You are friends with Jacob'
    })
    _status = 201

    mocking_response = self.app.response_class(
        response=_response,
        status=_status,
        mimetype='application/json'
    )
    return mocking_response

def mocking_response_remove_friend_success(self):
    _response = json.dumps({
        'status': 'success',
        'message': 'You are no longer friends with Jacob'
    })
    _status = 201

    mocking_response = self.app.response_class(
        response=_response,
        status=_status,
        mimetype='application/json'
    )
    return mocking_response


class TestFriend(BaseTestCase):

    def test_add_new_friend_controller_success(self):
        expected_output = mocking_response_add_friend_success(self)
        self.mock_save_controller.return_value = expected_output
        expected_output_dict = json.loads(expected_output.data.decode('utf-8'))

        user_response = self.client.post('/friends/', json=payload)
        content_type = user_response.content_type

        self.assertIn('application/json', content_type)
        self.assertEqual(expected_output_dict['status'], 'success')
        self.assertEqual(expected_output_dict['message'], 'You are friends with Jacob')
        self.assertEqual(user_response.status_code, 201)
        self.assertEqual(user_response, expected_output)
        self.assertEqual(len(self.mock_save_controller.mock_calls), 1)

    def test_add_new_friend_controller_fail_requestor_not_found(self):
        expected_output = mocking_response_add_friend_exceptions(self, 'requestor_not_found')
        self.mock_save_controller.return_value = expected_output
        expected_output_dict = json.loads(expected_output.data.decode('utf-8'))

        user_response = self.client.post('/friends/', json=payload)
        content_type = user_response.content_type

        self.assertIn('application/json', content_type)
        self.assertEqual(expected_output_dict['status'], 'fail')
        self.assertEqual(expected_output_dict['message'], 'Current profile is not found')
        self.assert404(user_response)
        self.assertEqual(user_response, expected_output)
        self.assertEqual(len(self.mock_save_controller.mock_calls), 1)

    def test_add_new_friend_controller_fail_receiver_not_found(self):
        expected_output = mocking_response_add_friend_exceptions(self, 'receiver_not_found')
        self.mock_save_controller.return_value = expected_output
        expected_output_dict = json.loads(expected_output.data.decode('utf-8'))

        user_response = self.client.post('/friends/', json=payload)
        content_type = user_response.content_type

        self.assertIn('application/json', content_type)
        self.assertEqual(expected_output_dict['status'], 'fail')
        self.assertEqual(expected_output_dict['message'], 'Friend''s account is not found')
        self.assert404(user_response)
        self.assertEqual(user_response, expected_output)
        self.assertEqual(len(self.mock_save_controller.mock_calls), 1)

    def test_remove_friend_controller_success(self):
        expected_output = mocking_response_remove_friend_success(self)
        self.mock_update_controller.return_value = expected_output
        expected_output_dict = json.loads(expected_output.data.decode('utf-8'))

        user_response = self.client.put('/friends/', json=payload)
        content_type = user_response.content_type

        self.assertIn('application/json', content_type)
        self.assertEqual(expected_output_dict['status'], 'success')
        self.assertEqual(expected_output_dict['message'], 'You are no longer friends with Jacob')
        self.assertEqual(user_response.status_code, 201)
        self.assertEqual(user_response, expected_output)
        self.assertEqual(len(self.mock_update_controller.mock_calls), 1)

    def test_remove_friend_controller_fail_requestor_not_found(self):
        expected_output = mocking_response_remove_friend_exceptions(self, 'requestor_not_found')
        self.mock_update_controller.return_value = expected_output
        expected_output_dict = json.loads(expected_output.data.decode('utf-8'))

        user_response = self.client.put('/friends/', json=payload)
        content_type = user_response.content_type

        self.assertIn('application/json', content_type)
        self.assertEqual(expected_output_dict['status'], 'fail')
        self.assertEqual(expected_output_dict['message'], 'Current profile is not found')
        self.assert404(user_response)
        self.assertEqual(user_response, expected_output)
        self.assertEqual(len(self.mock_update_controller.mock_calls), 1)

    def test_remove_friend_controller_fail_requestor_equal_friend(self):
        expected_output = mocking_response_remove_friend_exceptions(self, 'requestor_equal_friend')
        self.mock_update_controller.return_value = expected_output
        expected_output_dict = json.loads(expected_output.data.decode('utf-8'))

        user_response = self.client.put('/friends/', json=payload)
        content_type = user_response.content_type

        self.assertIn('application/json', content_type)
        self.assertEqual(expected_output_dict['status'], 'fail')
        self.assertEqual(expected_output_dict['message'], 'You cannot friend yourself')
        self.assert404(user_response)
        self.assertEqual(user_response, expected_output)
        self.assertEqual(len(self.mock_update_controller.mock_calls), 1)