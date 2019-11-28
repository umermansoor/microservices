import unittest
import requests
import json
from services import bookings
bookings.testing = True

class TestBookingService(unittest.TestCase):
    def setUp(self):
        self.url = "http://localhost:5003/bookings"

    def test_booking_records(self):
        """ Test /bookings/<username> """
        for b in good_responses:
            booking = json.dumps(b)
            response = requests.get(f"{self.url}/{b['user']}")
            reply = response.json()
            self.assertEqual(booking,reply)


    def test_new_booking(self):
        """ Test for booking creation """
        # manda o json de um booking fake
        username = "2"
        date = "20151201"
        movie = "3"
        fake_booking_data = [{"date": date, "movie": movie, "user": username}]
        fake_booking = json.dumps(fake_booking_data)

        # add_booking is a method to be defined later
        with bookings.new_booking() as new_booking:
            # send data as POST form to endpoint
            result = new_booking.post(f'/{username}', data=fake_booking_data)
            # check result from server with expected fake booking
            self.assertEqual(result.data, fake_booking)

    def test_not_found(self):
        """ Test /showtimes/<date> for non-existent users"""
        invalid_user = "999"
        actual_reply = requests.get(f"{self.url}/{invalid_user}")
        self.assertEqual(actual_reply.status_code, 404,
                         "Got {} but expected 404".format(
                             actual_reply.status_code))


b1 = { "user":1, "date":"2019-11-01", "movie":1 }
b2 = { "user":2, "date":"2019-11-02", "movie":2 }
b3 = { "user":3, "date":"2019-11-03", "movie":3 }
good_responses = [b1, b2, b3]

if __name__ == "__main__":
    unittest.main()
