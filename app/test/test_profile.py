import json
from app.test.base import BaseTestCase

payload = {
    "account_id": 1,
    "first_name": "Yan",
    "last_name": "Simon",
    "friendly_name": "YSimon",
    "city": "Atlanta",
    "state": "Georgia",
    "date_of_birth": "11/24/1987",
    "skillset_id": "beginner",
    "gender": "male"
}

def mocking_get_response_profile(self, is_empty):
    if is_empty:
        _response = json.dumps({"data": []})
        _status = 404
    else:
        _response = json.dumps({"data": [
            {
                "account_id": 1,
                "first_name": "Yan",
                "last_name": "Simon",
                "friendly_name": "YSimon",
                "city": "Atlanta",
                "state": "Georgia",
                "date_of_birth": "11/24/1987",
                "skillset_id": "beginner",
                "gender": "male",
                "achiever_pct": "6.5%",
                "explorer_pct": "12.8%",
                "killer_pct": "56%",
                "socializer_pct": "24.7%",
                "id": "4"
            }
        ]})
        _status = 200

    mocking_response = self.app.response_class(
        response=_response,
        status=_status,
        mimetype='application/json'
    )
    return mocking_response


def mocking_post_response_profile(self, status):
    if status == 'success':
        _response = json.dumps({'status': 'success',
                                'message': 'Successfully registered.',
                                'account_id': ""})
        _status = 201
    else:
        _response = json.dumps({'status': 'fail',
                                'message': 'Profile already exists.'})
        _status = 500

    mocking_response = self.app.response_class(
        response=_response,
        status=_status,
        mimetype='application/json'
    )
    return mocking_response


def mocking_get_response_friends(self, status):
    if status == 'success':
        _response = json.dumps({"data": [
            {
                "account_id": 1,
                "first_name": "Yan",
                "last_name": "Simon",
                "friendly_name": "YSimon",
                "city": "Atlanta",
                "state": "Georgia",
                "date_of_birth": "11/24/1987",
                "skillset_id": "beginner",
                "gender": "male",
                "achiever_pct": "6.5%",
                "explorer_pct": "12.8%",
                "killer_pct": "56%",
                "socializer_pct": "24.7%",
                "id": "4",
                "friend_id": "2"
            }
        ]})
        _status = 200

    else:
        _response = json.dumps({"data": []})
        _status = 404

    mocking_response = self.app.response_class(
        response=_response,
        status=_status,
        mimetype='application/json'
    )
    return mocking_response


class TestProfile(BaseTestCase):
    def test_list_profile_controller(self):
        expected_output = mocking_get_response_profile(self, False)
        self.mock_get_list_controller.return_value = expected_output
        expected_output_dict = json.loads(expected_output.data.decode('utf-8'))

        user_response = self.client.get('/profile/')

        content_type = user_response.content_type

        self.assertIn('application/json', content_type)
        self.assert200(user_response)
        self.assertEqual(user_response.json, expected_output_dict)
        self.assertEqual(len(user_response.json['data']), 1)
        self.mock_get_list_controller.assert_called_once()

    def test_get_profile_by_id_controller_success(self):
        expected_output = mocking_get_response_profile(self, False)
        self.mock_get_list_controller.return_value = expected_output
        expected_output_dict = json.loads(expected_output.data.decode('utf-8'))

        user_response = self.client.get('/profile/1')
        content_type = user_response.content_type

        self.assertIn('application/json', content_type)
        self.assert200(user_response)
        self.assertEqual(user_response.json, expected_output_dict)
        self.assertEqual(len(user_response.json['data']), 1)
        self.assertEqual(len(self.mock_get_list_controller.mock_calls), 1)

    def test_get_profile_by_id_controller_fail(self):
        expected_output = mocking_get_response_profile(self, True)
        self.mock_get_list_controller.return_value = expected_output
        user_response = self.client.get('/profile/1')
        self.assert404(user_response)
        self.assertEqual(len(user_response.json['data']), 0)
        self.assertEqual(len(self.mock_get_list_controller.mock_calls), 1)

    def test_save_new_profile_controller_success(self):
        expected_output = mocking_post_response_profile(self, 'success')
        self.mock_save_controller.return_value = expected_output
        expected_output_dict = json.loads(expected_output.data.decode('utf-8'))

        user_response = self.client.post('/profile/', json=payload)
        content_type = user_response.content_type

        self.assertIn('application/json', content_type)
        self.assertEqual(expected_output_dict['status'], 'success')
        self.assertEqual(user_response.status_code, 201)
        self.assertEqual(user_response, expected_output)
        self.assertEqual(len(self.mock_save_controller.mock_calls), 1)

    def test_save_new_profile_controller_fail(self):
        expected_output = mocking_post_response_profile(self, 'fail')
        self.mock_save_controller.return_value = expected_output
        user_response = self.client.post('/profile/', json=payload)
        self.assertEqual(user_response.status_code, 500)
        self.assertEqual(len(self.mock_save_controller.mock_calls), 1)

    def test_update_profile_controller_success(self):
        expected_output = mocking_post_response_profile(self, 'success')
        self.mock_update_controller.return_value = expected_output
        expected_output_dict = json.loads(expected_output.data.decode('utf-8'))

        user_response = self.client.put('/profile/', json=payload)
        content_type = user_response.content_type

        self.assertIn('application/json', content_type)
        self.assertEqual(expected_output_dict['status'], 'success')
        self.assertEqual(user_response.status_code, 201)
        self.assertEqual(user_response, expected_output)
        self.assertEqual(len(self.mock_update_controller.mock_calls), 1)

    def test_update_profile_controller_fail(self):
        expected_output = mocking_post_response_profile(self, 'fail')
        self.mock_update_controller.return_value = expected_output
        user_response = self.client.put('/profile/', json=payload)
        self.assertEqual(user_response.status_code, 500)
        self.assertEqual(len(self.mock_update_controller.mock_calls), 1)

    def test_get_profile_friends_success(self):
        expected_output = mocking_get_response_friends(self, 'success')
        self.mock_get_list_controller.return_value = expected_output
        expected_output_dict = json.loads(expected_output.data.decode('utf-8'))
        user_response = self.client.get('/profile/friends/1')
        content_type = user_response.content_type

        self.assertIn('application/json', content_type)
        self.assert200(user_response)
        self.assertEqual(user_response.json, expected_output_dict)
        self.assertEqual(len(user_response.json['data']), 1)
        self.assertEqual(len(self.mock_get_list_controller.mock_calls), 1)

    def test_get_profile_friends_fail(self):
        expected_output = mocking_get_response_friends(self, 'fail')
        self.mock_get_list_controller.return_value = expected_output
        expected_output_dict = json.loads(expected_output.data.decode('utf-8'))
        user_response = self.client.get('/profile/friends/1')
        content_type = user_response.content_type

        self.assertIn('application/json', content_type)
        self.assert404(user_response)
        self.assertEqual(user_response.json, expected_output_dict)
        self.assertEqual(len(user_response.json['data']), 0)
        self.assertEqual(len(self.mock_get_list_controller.mock_calls), 1)
