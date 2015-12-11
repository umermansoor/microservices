import unittest
import requests


class TestShowTimesService(unittest.TestCase):
    def setUp(self):
        self.url = "http://127.0.0.1:5002/showtimes"

    def test_showtimes_records(self):
        """ Test /showtimes/<date> for all known showtimes"""
        for date, expected in GOOD_RESPONSES.iteritems():
            reply = requests.get("{}/{}".format(self.url, date))
            actual_reply = reply.json()

            self.assertEqual(len(actual_reply), len(expected),
                             "Got {} showtimes but expected {}".format(
                                 len(actual_reply), len(expected)
                             ))

            # Use set because the order doesn't matter
            self.assertEqual(set(actual_reply), set(expected),
                             "Got {} but expected {}".format(
                                 actual_reply, expected))


    def test_not_found(self):
        """ Test /showtimes/<date> for non-existent dates"""
        invalid_date = 20490101
        actual_reply = requests.get("{}/{}".format(self.url, invalid_date))
        self.assertEqual(actual_reply.status_code, 404,
                         "Got {} but expected 404".format(
                             actual_reply.status_code))

GOOD_RESPONSES = {
    "20151130": [
        "720d006c-3a57-4b6a-b18f-9b713b073f3c",
        "a8034f44-aee4-44cf-b32c-74cf452aaaae",
        "39ab85e5-5e8e-4dc5-afea-65dc368bd7ab"
    ],
    "20151201": [
        "267eedb8-0f5d-42d5-8f43-72426b9fb3e6",
        "7daf7208-be4d-4944-a3ae-c1c2f516f3e6",
        "39ab85e5-5e8e-4dc5-afea-65dc368bd7ab",
        "a8034f44-aee4-44cf-b32c-74cf452aaaae"
    ],
    "20151202": [
        "a8034f44-aee4-44cf-b32c-74cf452aaaae",
        "96798c08-d19b-4986-a05d-7da856efb697",
        "39ab85e5-5e8e-4dc5-afea-65dc368bd7ab",
        "276c79ec-a26a-40a6-b3d3-fb242a5947b6"
    ],
    "20151203": [
        "720d006c-3a57-4b6a-b18f-9b713b073f3c",
        "39ab85e5-5e8e-4dc5-afea-65dc368bd7ab"
    ],
    "20151204": [
        "96798c08-d19b-4986-a05d-7da856efb697",
        "a8034f44-aee4-44cf-b32c-74cf452aaaae",
        "7daf7208-be4d-4944-a3ae-c1c2f516f3e6"
    ],
    "20151205": [
        "96798c08-d19b-4986-a05d-7da856efb697",
        "a8034f44-aee4-44cf-b32c-74cf452aaaae",
        "7daf7208-be4d-4944-a3ae-c1c2f516f3e6",
        "276c79ec-a26a-40a6-b3d3-fb242a5947b6",
        "39ab85e5-5e8e-4dc5-afea-65dc368bd7ab"
    ]
}

if __name__ == "__main__":
    unittest.main()
