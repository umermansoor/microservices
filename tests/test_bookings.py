import unittest
import requests
import json
from services import bookings
from datetime import date as datetime_date
bookings.testing = True


class TestBookingService(unittest.TestCase):
    def setUp(self):
        self.url = "http://localhost:5003/bookings"
        self.post_url = "http://localhost:5003/bookings/new"

    def test_booking_records(self):
        """ Test /bookings/<username> """
        for booking in good_responses:
            response = requests.get(f"{self.url}/{booking['user']}")
            reply = response.json()
            self.assertEqual(booking, reply)


    def test_new_booking(self):
        """ Test for booking creation """
        username = "2"
        date = datetime_date(2019,12,12)
        movie = "3"
        fake_booking_data = {"date": date, "movie": movie, "user": username}
        fake_booking = bookings.booking_schema.dumps(fake_booking_data)

        with bookings.new_booking() as new_booking:
            # send data as POST form to endpoint
            result = new_booking.post(self.post_url, data=fake_booking_data)
            # check result from server with expected fake booking
            self.assertEqual(result.data, fake_booking)


    def test_not_found(self):
        """ Test /showtimes/<date> for non-existent users"""
        invalid_user = "999"
        actual_reply = requests.get(f"{self.url}/{invalid_user}")
        self.assertEqual(actual_reply.status_code, 404,
                         "Got {} but expected 404".format(
                             actual_reply.status_code))


#b1 = { "user":1, "date":"2019-11-01", "movie":1 }
b2 = [{ "user":2, "date":"2019-11-02", "movie":2 }]
b3 = [{ "user":3, "date":"2019-11-03", "movie":3 }]
good_responses = [b2, b3]

if __name__ == "__main__":
    unittest.main()
