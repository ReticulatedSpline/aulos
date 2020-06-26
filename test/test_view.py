import sys
import os
import unittest
import datetime

testdir = os.path.dirname(__file__)
srcdir = '../src'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))
from view import View


class TestViewMethods(unittest.TestCase):

    def setUp(self):
        self.view = View()

    def test_strfdelta(self):
        tdelta = datetime.timedelta(seconds=10)
        self.assertEqual(self.view._strfdelta(tdelta, 'FOO'))

