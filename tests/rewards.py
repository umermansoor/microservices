import unittest
import requests


class TestRewardService(unittest.TestCase):
	""" This tests the Reward cinema service """
    def setUp(self):
        self.url = "http://127.0.0.1:5004/rewards"
        self.add_score_url = "http://127.0.0.1:5004/rewards/add_point/"
        self.is_prize_available_url = "http://127.0.0.1:5004/rewards/is_prize_available/"
        self.GOOD_RESPONSES ={
		  "chris_rivers": 1,
		  "garret_heaton": 2,
		  "dwight_schrute": 4
		}

    def test_user_reward_score(self):
    	""" This method assets that a user has the right score"""

        for username, expected_reply in self.GOOD_RESPONSES.items():
            actual_reply = requests.get("{}/{}".format(self.url, username))
            actual_reply = actual_reply.json()

            self.assertEqual(actual_reply, expected_reply,
                             f"Got {actual_reply} points but expected {expected_reply} points as score")


    def test_add_point_to_user_score(self):
    	""" This asserts that a new point is computed correctly"""
    	username = "chris_rivers"
    	previous_score = self.GOOD_RESPONSES['chris_rivers']
    	expected_reply = {"chris_rivers" : previous_score + 1}
    	response = requests.get(f"{self.add_score_url}/{username}")
    	actual_reply = response.json()

    	self.assertEqual(actual_reply, expected_reply,
    		f"Got {actual_reply} points but expected {expected_reply} points as the new score")


	def test_is_prize_available(self):
		""" This asserts one can only get a prize if one has enough points"""
		username = 'dwight_schrute'
		score = self.GOOD_RESPONSES[username]
		expected_reply = {username : True}
		response = requests.get(f"{self.is_prize_available_url}/{username}")
		actual_reply = response.json()

		self.assertEqual(actual_reply, expected_reply,
    		f"Got {actual_reply} but expected {expected_reply} ")




