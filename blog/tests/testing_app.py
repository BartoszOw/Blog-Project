import unittest
from flask import session
from blog import app
from blog.routes import login_required


class TestingApplication(unittest.TestCase):

    def setUp(self):
        self.app = app

    # Test, który sprawdza, czy przekierowanie na stronę logowania wymaga parametru "next"
    def test_login_required_redirects_to_login_with_next_parameter(self):
            with self.app.test_client() as client:
                response = client.get('/new_post')
                self.assertEqual(response.status_code, 302)
                self.assertTrue(response.location.endswith('/login?next=/new_post'))

     # Test, który sprawdza, czy strony wymagające logowania przekierowują na stronę logowania
    def test_managment_requires_login(self):
        routes = ['/new_post', '/edit_entry/1', '/delete_entry/1']
        for route in routes:
            with self.app.test_request_context(route):
                session['logged_in'] = False
                response = login_required(lambda: None)()

                self.assertEqual(response.status_code, 302)
                self.assertEqual(response.location, '/login?next=' + route)

    # Test, który sprawdza, czy strona z listą nieopublikowanych wpisów wymaga logowania
    def test_unpublished_list_need_login(self):
        with self.app.test_request_context('/unpublished_list'):
            session['logged_in'] = False
            response = login_required(lambda: None)()

            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.location, '/login?next=/unpublished_list')

    # Test, który sprawdza, czy na stronie z listą nieopublikowanych wpisów są tylko nieopublikowane wpisy
    def test_unpublished_list_show_only_unpublished_entries(self):
        with self.app.test_client() as client:
            with client.session_transaction() as sess:
                sess['logged_in'] = True
            response = client.get('/unpublished_list')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Unpublished', response.data)
            self.assertNotIn(b'Published', response.data)

    # Test, który sprawdza, czy na stronie głównej są tylko opublikowane wpisy
    def test_homepage_show_only_published_entries(self):
        with self.app.test_client() as client:
            response = client.get('/')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Published', response.data)
            self.assertNotIn(b'Unpublished', response.data)

    # Test, który sprawdza, czy aplikacja wywołuje 404, gdy brakuje identyfikatora wpisu
    def test_app_abort_404_if_entry_id_is_none(self):
        with self.app.test_client() as client:
            response = client.get('/post/100')
            self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()