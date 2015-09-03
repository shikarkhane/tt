'''
Created on Nov 12, 2014

@author: nikhil
'''
import unittest
from db._message import Message
from random import randint
from db._timesplit import TimeInAndOut, Timesplit
import json
import redis
import settings

pool = [redis.ConnectionPool(host=s["server"], port=s["port"], db=0) for s in settings.REDIS_SHARDS]

class Test_Message(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass
    def test_message_values(self):
        a,b,c,d,e,f,g = 'user-A','user-B',20141112101010,23,"hello",14,False
        i = [a,b,c,d,e,f,g]
        m = Message(a,b,c,d,e,f,g)
        o = [m.from_user, m.to_user, m.send_timestamp, m.trinket_name, m.text, m.seconds_sent, m.unread]
        self.assertEqual(i, o)
    def test_message_key_value(self):
        a,b,c,d,e,f,g = 'user-A','user-B',20141112101010,23,"hello",14, False
        i = [a,b,c,d,e,f,g]
        k, v = 'message:{0}:{1}:{2}'.format(a,b,c), json.dumps({"text":e, "trinket_name":d, "seconds_sent": f,
                                                                "unread": g})
        m = Message(k,v)
        o = [m.from_user, m.to_user, m.send_timestamp, m.trinket_name, m.text, m.seconds_sent, m.unread]
        self.assertEqual(i, o)
class Test_TimeInOut(unittest.TestCase):
    def setUp(self):
        self.user = randint(10000000, 100000000)
        self.user_pair = randint(10000000, 100000000)
        self.time_in = randint(1, 10000)
        self.time_out = randint(1,10000)
        self.io = TimeInAndOut(pool)
    def tearDown(self):
        self.io.remove(self.user)
    def test_save_get_remove(self):
        io = self.io
        io.remove(self.user)
        self.assertEqual( io.get(self.user), False)
        self.assertEqual(io.save(self.user, self.time_in, self.time_out), True)
        self.assertNotEqual( io.get(self.user), False)
    def test_check_saved_value(self):
        io = self.io
        io.remove(self.user)
        self.assertEqual( io.get(self.user), False)
        if io.save(self.user, self.time_in, self.time_out):
            res = Timesplit(io.get(self.user))
            self.assertEqual( res.time_in, self.time_in)
            self.assertEqual( res.time_out, self.time_out)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()