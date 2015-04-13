# encoding:utf-8
import os
import sys

util_dir = os.path.join(os.path.dirname(__name__), '..')
if util_dir is not sys.path:
    sys.path.append(util_dir)


import unittest
from utils.binary import writeBool, readBool


class BinaryTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_read_write_bool(self):
        self.assertEqual(readBool(writeBool(True)), True)
        self.assertEqual(readBool(writeBool(False)), False)


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(BinaryTest('test_read_write_bool'))
    unittest.TextTestRunner().run(suite)
