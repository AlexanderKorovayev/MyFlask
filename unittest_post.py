import requests
import unittest
from app import app, handle_post_users, handle_get_users
import multiprocessing
import threading


class TestPostRequest(unittest.TestCase):
    
    def setUp(self):
        self.post_address = 'http://localhost:2000/users?name=Vasya&age=26'
        self.headers = {'Host': 'localhost',
                        'Accept': 'application/json; charset=utf-8'}
        self.p = threading.Thread(target=app.run, daemon=True)
        self.p.start()

    def test_post(self):
        r = requests.post(url=self.post_address,
                          headers=self.headers)
        self.assertEqual(r.reason, 'Created')
        self.assertEqual(r.status_code, 204)


if __name__ == '__main__':
    unittest.main()