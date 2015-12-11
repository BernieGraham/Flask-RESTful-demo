#!venv/bin/python

import unittest
import requests
import json
import rest
import thread

class TestRestServer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass
        # thread.start_new_thread(rest.app.run, ())

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_users(self):

        # no users
        url = 'http://localhost:5000/users/jsmith'
        r = requests.get(url)
        self.assertEqual(r.status_code, 404)

        # add user
        url = 'http://localhost:5000/users'
        payload = {
            "first_name": "Joe",
            "last_name": "Smith",
            "userid": "jsmith",
            "groups": ["admins", "users"]
        }
        headers = {'content-type': 'application/json'}
        r = requests.post(url, data=json.dumps(payload), headers=headers)
        self.assertEqual(r.status_code, 204)

        # read added user
        url = 'http://localhost:5000/users/jsmith'
        r = requests.get(url)
        self.assertEqual(r.status_code, 200)

        # modify user
        url = 'http://localhost:5000/users/jsmith'
        payload = {
            "first_name": "Joey",
            "last_name": "Smithy",
            "userid": "jsmith",
            "groups": ["admins"]
        }
        headers = {'content-type': 'application/json'}
        r = requests.put(url, data=json.dumps(payload), headers=headers)
        self.assertEqual(r.status_code, 204)

        # read added user
        url = 'http://localhost:5000/users/jsmith'
        r = requests.get(url)
        self.assertEqual(r.status_code, 200)

        # delete user
        url = 'http://localhost:5000/users/jsmith'
        r = requests.delete(url)
        self.assertEqual(r.status_code, 204)

    def test_groups(self):

        # create a new group
        url = 'http://localhost:5000/groups'
        r = requests.post(url, data={"name":"testGroup"})
        self.assertEqual(r.status_code, 204)

        # check for duplicate posting
        r = requests.post(url, data={"name":"testGroup"})
        self.assertEqual(r.status_code, 409)

        # add user
        url = 'http://localhost:5000/users'
        payload = {
            "first_name": "Sarah",
            "last_name": "Smith",
            "userid": "ssmith",
            "groups": ["admins", "users"]
        }
        headers = {'content-type': 'application/json'}
        r = requests.post(url, data=json.dumps(payload), headers=headers)
        self.assertEqual(r.status_code, 204)

        # add user
        url = 'http://localhost:5000/users'
        payload = {
            "first_name": "Yoshi",
            "last_name": "Smith",
            "userid": "ysmith",
            "groups": ["admins", "users"]
        }
        headers = {'content-type': 'application/json'}
        r = requests.post(url, data=json.dumps(payload), headers=headers)
        self.assertEqual(r.status_code, 204)

        # get group for testGroup
        url = 'http://localhost:5000/groups/testGroup'
        r = requests.get(url)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(json.loads(r.content)), 0)

        # get group for admins
        url = 'http://localhost:5000/groups/admins'
        r = requests.get(url)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(json.loads(r.content)), 2)

        # delete group admins
        url = 'http://localhost:5000/groups/admins'
        r = requests.delete(url)
        self.assertEqual(r.status_code, 204)

if __name__ == '__main__':
    unittest.main()
