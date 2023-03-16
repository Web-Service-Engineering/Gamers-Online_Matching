from flask_testing import TestCase
from app.main import db
from manage import app
from unittest.mock import patch, Mock


class BaseTestCase(TestCase):
    """ Base Tests """

    def create_app(self):
        app.config.from_object('app.main.config.TestingConfig')
        return app

    def setUp(self):
        self.mock_get_requests = patch('flask.testing.FlaskClient.get')
        self.mock_post_requests = patch('flask.testing.FlaskClient.post')
        self.mock_put_requests = patch('flask.testing.FlaskClient.put')

        self.mock_get_list_controller = self.mock_get_requests.start()
        self.mock_save_controller = self.mock_post_requests.start()
        self.mock_update_controller = self.mock_put_requests.start()

    def tearDown(self):
        self.mock_get_requests.stop()
        self.mock_post_requests.stop()
        self.mock_put_requests.stop()
