import unittest
import requests


class TestUserService(unittest.TestCase):
    def setUp(self):
        self.url = "http://127.0.0.1:5000/users"

    def test_user_records(self):
        for username, expected in GOOD_RESPONSES.iteritems():
            actual_reply = requests.get("{}/{}".format(self.url, username))
            actual_reply = actual_reply.json()

            self.assertEqual(actual_reply, expected,
                             "Got {} user record but expected {}".format(
                                 actual_reply, expected
                             ))

    def test_user_not_found(self):
        """ Test /users/<username> for non-existent user"""
        invalid_user = "jim_the_duck_guy"
        actual_reply = requests.get("{}/{}".format(self.url, invalid_user))
        self.assertEqual(actual_reply.status_code, 404,
                         "Got {} but expected 404".format(
                             actual_reply.status_code))

GOOD_RESPONSES = {
  "chris_rivers" : {
    "id": "chris_rivers",
    "name": "Chris Rivers",
    "last_active":1360031010
  },
  "peter_curley" : {
    "id": "peter_curley",
    "name": "Peter Curley",
    "last_active": 1360031222
  },
  "garret_heaton" : {
    "id": "garret_heaton",
    "name": "Garret Heaton",
    "last_active": 1360031425
  },
  "michael_scott" : {
    "id": "michael_scott",
    "name": "Michael Scott",
    "last_active": 1360031625
  },
  "jim_halpert" : {
    "id": "jim_halpert",
    "name": "Jim Halpert",
    "last_active": 1360031325
  },
  "pam_beesly" : {
    "id": "pam_beesly",
    "name": "Pam Beesly",
    "last_active": 1360031225
  },
  "dwight_schrute" : {
    "id": "dwight_schrute",
    "name": "Dwight Schrute",
    "last_active": 1360031202
  }
}

if __name__ == "__main__":
    unittest.main()
