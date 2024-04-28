import unittest
from key_handler import create_key, get_key
from time import time, sleep
import math

class TestRelease(unittest.TestCase):
    def test_too_soon(self):
        response = create_key(release_date=math.floor(time()+60*60))
        with self.assertRaises(Exception) as cm:
            get_key(uuid=response['uuid'], secret=response['secret'])
        self.assertEqual(str(cm.exception), 'Too soon to release key')

    def test_release(self):
        SECONDS_TO_WAIT = 5
        response = create_key(release_date=math.floor(time()+SECONDS_TO_WAIT))
        sleep(SECONDS_TO_WAIT)
        response = get_key(uuid=response['uuid'], secret=response['secret'])
        self.assertIs(type(response['private_key']), str)