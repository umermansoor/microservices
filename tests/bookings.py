import unittest
import requests


class TestBookingService(unittest.TestCase):
    def setUp(self):
        self.url = "http://127.0.0.1:5003/bookings"

    def test_booking_records(self):
        """ Test /bookings/<username> for all known bookings"""
        for date, expected in GOOD_RESPONSES.iteritems():
            reply = requests.get("{}/{}".format(self.url, date))
            actual_reply = reply.json()

            self.assertEqual(len(actual_reply), len(expected),
                             "Got {} booking but expected {}".format(
                                 len(actual_reply), len(expected)
                             ))

            # Use set because the order doesn't matter
            self.assertEqual(set(actual_reply), set(expected),
                             "Got {} but expected {}".format(
                                 actual_reply, expected))

    def test_not_found(self):
        """ Test /showtimes/<date> for non-existent users"""
        invalid_user = "jim_the_duck_guy"
        actual_reply = requests.get("{}/{}".format(self.url, invalid_user))
        self.assertEqual(actual_reply.status_code, 404,
                         "Got {} but expected 404".format(
                             actual_reply.status_code))

GOOD_RESPONSES = {
  "chris_rivers": {
    "20151201": [
      "267eedb8-0f5d-42d5-8f43-72426b9fb3e6"
    ]
  },
  "garret_heaton": {
    "20151201": [
      "267eedb8-0f5d-42d5-8f43-72426b9fb3e6"
    ],
    "20151202": [
      "276c79ec-a26a-40a6-b3d3-fb242a5947b6"
    ]
  },
  "dwight_schrute": {
    "20151201": [
      "7daf7208-be4d-4944-a3ae-c1c2f516f3e6",
      "267eedb8-0f5d-42d5-8f43-72426b9fb3e6"
    ],
    "20151205": [
      "a8034f44-aee4-44cf-b32c-74cf452aaaae",
      "276c79ec-a26a-40a6-b3d3-fb242a5947b6"
    ]
  }
}

if __name__ == "__main__":
    unittest.main()
