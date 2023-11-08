import unittest
from unittest.mock import MagicMock

from Swearing.swearing import contains_swears

class SwearingTests(unittest.TestCase):
    def test_swear_detection(self):        
        #r"b+a+s+t+a+r+d+",
        self.assertTrue(contains_swears("bastard"))
        self.assertTrue(contains_swears("baaaaaaaastard"))
        #r"\ba+ss+(?:hole)?\b",
        self.assertTrue(contains_swears("ass"))
        self.assertTrue(contains_swears("assssss"))
        self.assertTrue(contains_swears("asshole"))
        self.assertFalse(contains_swears("glass"))
        self.assertFalse(contains_swears("assist"))
        #r"\ba+ss+e+s\b",
        self.assertTrue(contains_swears("asses"))
        self.assertTrue(contains_swears("asssssses"))
        self.assertFalse(contains_swears("assess"))
        self.assertFalse(contains_swears("assessment"))
        #r"\ba+r+s+e+s?(?:hole)?\b",
        self.assertTrue(contains_swears("arse"))
        self.assertTrue(contains_swears("arses"))
        self.assertFalse(contains_swears("parse"))
        #r"\bb+a+d+a+ss+",	
        self.assertTrue(contains_swears("badass"))
        self.assertTrue(contains_swears("badasses"))
        #r"^hell([^o]|\b)|[^s]h+el+l([^o]|\b)",
        self.assertTrue(contains_swears("hell"))
        self.assertFalse(contains_swears("hello"))
        self.assertFalse(contains_swears("shell"))
        #r"([^slue]|\b)t+w+a+t+",    
        self.assertTrue(contains_swears("twat"))
        self.assertFalse(contains_swears("pocketwatch"))        


