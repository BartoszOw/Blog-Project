import unittest
from flask import session
from flask.testing import FlaskClient
from werkzeug.datastructures import ImmutableDict
from werkzeug.test import EnvironBuilder
from blog import app
from blog.routes import login_required

class TestLoginRequired(unittest.TestCase):

    def setUp(self):
        self.app = app

    def test_login_required_redirects_to_login_with_next_parameter(self):
        with self.app.test_request_context('/some-page'):
            @self.app.route('/login')
            def test_login_page():
                return 'Login Page'

            @self.app.route('/some-page')
            @login_required
            def test_some_page():
                return 'Some Page'

            with self.app.test_client() as client:
                response = client.get('/some-page')
                self.assertEqual(response.status_code, 302)
                self.assertTrue(response.location.endswith('/login?next=/some-page'))

if __name__ == '__main__':
    unittest.main()