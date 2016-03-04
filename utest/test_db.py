'''
Created on Nov 12, 2014

@author: nikhil
'''
import unittest
from db._message import Message, Message_Data
from db._trinket import Animation
from libs.message import save_message
from random import randint
from db._timesplit import TimeInAndOut, Timesplit
import json
#import redis
import settings
from rediscluster import StrictRedisCluster

#pool = [redis.ConnectionPool(host=s["server"], port=s["port"], db=0) for s in settings.REDIS_SHARDS]
startup_nodes = [{"host": settings.REDIS_CLUSTER["server"], "port": settings.REDIS_CLUSTER["port"]}]
pool = StrictRedisCluster(startup_nodes=startup_nodes, decode_responses=True)

class Test_Trinket(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass
    def test_random_active(self):
        t = Animation(pool).get_random_active()
        self.assertNotEqual(t, None)
class Test_Message_data(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass
    def test_trim_conversation(self):
        a,b,c,d,e,f,g = 'user-A','user-B',20141112101018,23,"hello",14,False
        data = {"from_user" : a, "to_user" : b, "send_timestamp" : c, "trinket_name": d, "text": e,
                "seconds_sent": f, "unread" : g }
        save_message(pool, data)

        self.assertEqual(0, 1)
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
    def test_save_get_remove_pair(self):
        io = self.io
        io.remove_pair(self.user, self.user_pair)
        k,v = io.get_pair(self.user, self.user_pair)
        self.assertEqual( v , False)
        self.assertEqual(io.save_pair(self.user, self.user_pair, self.time_in, self.time_out), True)
        k,v =  io.get_pair(self.user, self.user_pair)
        self.assertNotEqual(v, False)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()