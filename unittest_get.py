import requests
import unittest
from app import app, handle_post_users, handle_get_users
import multiprocessing
import threading


class TestGetRequest(unittest.TestCase):
    
    def setUp(self):
        self.get_address = 'http://localhost:2000/users'
        self.headers = {'Host': 'localhost',
                        'Accept': 'application/json'}
        self.p = threading.Thread(target=app.run, daemon=True)
        self.p.start()

    def test_get(self):
        r = requests.get(url=self.get_address,
                          headers=self.headers)
        print(r.reason, r.status_code)
        self.assertEqual(r.reason, 'OK')
        self.assertEqual(r.status_code, 200)



if __name__ == '__main__':
    unittest.main()