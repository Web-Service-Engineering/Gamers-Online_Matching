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
        self.mock_account_list_requests_controller = patch('flask.testing.FlaskClient.get')
        self.mock_register_account_requests_controller = patch('flask.testing.FlaskClient.post')
        self.mock_get_account_list_controller = self.mock_account_list_requests_controller.start()
        self.mock_save_account_controller = self.mock_register_account_requests_controller.start()

    def tearDown(self):
        self.mock_account_list_requests_controller.stop()
        self.mock_register_account_requests_controller.stop()
