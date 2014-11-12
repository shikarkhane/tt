'''
Created on Nov 12, 2014

@author: nikhil
'''
import unittest
from db._message import Message

class Test_Message(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass
    def test_message_values(self):
        a,b,c,d,e = 'user-A','user-B',20141112101010,23,"hello"
        i = [a,b,c,d,e]
        m = Message(a,b,c,d,e)
        o = [m.from_user, m.to_user, m.send_timestamp, m.trinket_id, m.text]
        self.assertEqual(i, o)
    def test_message_key_value(self):
        a,b,c,d,e = 'user-A','user-B',20141112101010,23,"hello"
        i = [a,b,c,d,e]
        k, v = 'message:{0}:{1}:{2}'.format(a,b,c), '{0}|{1}'.format(d,e)
        m = Message(k,v)
        o = [m.from_user, m.to_user, m.send_timestamp, m.trinket_id, m.text]
        self.assertEqual(i, o)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()