import unittest
from unittest.mock import MagicMock

from Muzzle.muzzle_classes import MuzzleVictim, Muzzler

class MuzzleTests(unittest.TestCase):
    def test_muzzle_detection(self):
        me = MagicMock()
        muzzler = MagicMock()
        guild = MagicMock()
        victim = MuzzleVictim(me, 
            muzzle_type="dronify", 
            allowed_phrases=["this is a test"], muzzled_by=muzzler, 
            guild=guild, reason_muzzled="", struggle_allowed=False)
        self.assertTrue(victim.allowed_to_say("this is a test"))
        self.assertTrue(victim.allowed_to_say("This is a test"))
        self.assertTrue(victim.allowed_to_say("This is a test."))
        self.assertTrue(victim.allowed_to_say("This is a test!"))
        self.assertFalse(victim.allowed_to_say("Test."))
        victim = MuzzleVictim(me, 
            muzzle_type="dronify", 
            allowed_phrases=["test1","test2","test3"], muzzled_by=muzzler, 
            guild=guild, reason_muzzled="", struggle_allowed=False)
        self.assertTrue(victim.allowed_to_say("test1"))
        self.assertTrue(victim.allowed_to_say("test2"))
        self.assertTrue(victim.allowed_to_say("test3"))
        self.assertTrue(victim.allowed_to_say("test1 test2 test3"))
        self.assertTrue(victim.allowed_to_say("Test1, test2 test3! :)"))
        self.assertFalse(victim.allowed_to_say("test4"))
        
    def test_safeword_detection(self):
        me = MagicMock()
        muzzler = MagicMock()
        guild = MagicMock()
        victim = MuzzleVictim(me, 
            muzzle_type="dronify", 
            allowed_phrases=["this is a test"], muzzled_by=muzzler, 
            guild=guild, reason_muzzled="", struggle_allowed=False)
        self.assertTrue(victim.found_safeword("🟢"))
        self.assertTrue(victim.found_safeword("🟡"))
        self.assertTrue(victim.found_safeword("🔴"))
        self.assertTrue(victim.found_safeword("This is a test. 🟢"))        
        
    def test_muzzler_linking(self):
        me = MagicMock()        
        guild = MagicMock()
        muzzler = Muzzler(MagicMock(), MagicMock())
        victim = MagicMock()
        muzzler.add_victim(victim)
        self.assertEqual(len(muzzler.victims), 1)
        muzzler.remove_victim(victim)
        self.assertEqual(len(muzzler.victims), 0)

