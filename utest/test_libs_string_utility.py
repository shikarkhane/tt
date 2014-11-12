'''
Created on Nov 12, 2014

@author: nikhil
'''
import unittest
from libs.string_utility import split_by_first_occurance

class Test_String_Utility(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass
    def test_split_by_first_occurance(self):
        o = ['34', 'thisissecondtestcaseiamwritingintt']
        s = '|'.join(o)
        self.assertEqual(split_by_first_occurance(s,'|'), o)
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()