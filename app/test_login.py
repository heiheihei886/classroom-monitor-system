import unittest
from app.run import app
import json


class TestLogin(unittest.TestCase):
    def setUp(self):
        self.app = app
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_empty_name_password(self):
        response = self.client.post("/login", data={})
        resp_json = response.data
        resp_dict = json.loads(resp_json)
        self.assertIn("code", resp_dict)
        code = resp_dict.get("code")
        self.assertEqual(code, 65535)
        response = self.client.post("/login", data={"name": "admin"})
        resp_json = response.data
        resp_dict = json.loads(resp_json)
        self.assertIn("code", resp_dict)
        code = resp_dict.get("code")
        self.assertEqual(code, 65535)
        msg = resp_dict.get('message')
        self.assertEqual(msg, "Incomplete information")

    def test_wrong_name_password(self):
        response = self.client.post("/login", data={"name": "admin", "password": "123456789"})
        resp_json = response.data
        resp_dict = json.loads(resp_json)
        self.assertIn("code", resp_dict)
        code = resp_dict.get("code")
        self.assertEqual(code, 65535)
        msg = resp_dict.get('message')
        self.assertEqual(msg, "Wrong information")


if __name__ == '__main__':
    unittest.main()