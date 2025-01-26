import json
import unittest

from run import app


class TestLogin(unittest.TestCase):

    def setUp(self):
        self.app = app
        app.testing = True
        self.client=app.test_client()

    def test_empty_name_password(self):
        headers = {
            'Content-Type': 'application/json'
        }

        data = {
            'username': '',
            'password': ''
        }
        response = self.client.post('/login', headers=headers, data=json.dumps(data))
        resp_json = response.data
        print(resp_json)
        self.assertEqual(response.status_code, 400)

    def test_incorrect_name_password(self):
        headers = {
            'Content-Type': 'application/json'
        }

        data = {
            'username': 'test',
            'password': '123456',
            'captcha': '123456'
        }
        response = self.client.post('/login', headers=headers, data=json.dumps(data))
        resp_json = response.data
        print(resp_json)
        self.assertEqual(response.status_code, 401)

    def test_login_ok(self):
        headers = {
            'Content-Type': 'application/json'
        }

        data = {
            'username': 'test',
            'password': 'test123',
            'captcha': '123456'
        }
        response = self.client.post('/login', headers=headers, data=json.dumps(data))
        resp_json = response.data
        print(resp_json)
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
