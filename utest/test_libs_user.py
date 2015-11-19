'''
Created on Feb 12, 2015

@author: nikhil
'''
import unittest
from libs.user import are_on_network_plus_timesplit
import redis
import settings
import json

pool = [redis.ConnectionPool(host=s["server"], port=s["port"], db=0) for s in settings.REDIS_SHARDS]

class Test_User(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass
    def test_are_on_network_plus_timesplit(self):
        user = '+46705438947'
        x = {"contacts":[{"first_name":"Edd","last_name":"Huang","phone_number":"+46705438947","phone_type":None},
                         {"first_name":"Edith","last_name":"Jones","phone_number":"+46700907802","phone_type":None},
                         {"first_name":"Nikhil","last_name":"Talinger","phone_number":"2354531258","phone_type":None},
                         {"first_name":"Emanuel","last_name":"Lindberg","phone_number":"+0101010101","phone_type":None},
                         {"first_name":"Rajesh","last_name":"Gehlawat","phone_number":"+919610614914","phone_type":None},
                         {"first_name":"Rishi","last_name":"Khangwal","phone_number":"+919352427971","phone_type":None},
                         {"first_name":"Maneesh","last_name":"Jangid","phone_number":"+919549194555","phone_type":None}]}
        d = x["contacts"]
        r = are_on_network_plus_timesplit(pool, user, d)
        self.assertEquals(len(d), len(r))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()