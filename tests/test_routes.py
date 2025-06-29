import unittest
from app import app

class BasicRouteTests(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

        # Simulate login
        with self.app.session_transaction() as session:
            session['username'] = 'testuser'  # This bypasses login check

    def test_home_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_login_page(self):
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)

    def test_add_recipe_get(self):
        response = self.app.get('/add')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
