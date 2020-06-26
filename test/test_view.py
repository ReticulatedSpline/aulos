import datetime
import unittest
import typing
import src.cfg as cfg
from src.view import View


class TestViewMethods(unittest.TestCase):

    def test_strfdelta(self):
        tdelta = datetime.timedelta(seconds=0)
        self.assertEqual(View._strfdelta(tdelta), "0:00")
        tdelta = datetime.timedelta(seconds=10)
        self.assertEqual(View._strfdelta(tdelta), "0:10")
        tdelta = datetime.timedelta(minutes=1, seconds=30)
        self.assertEqual(View._strfdelta(tdelta), "1:30")
        tdelta = datetime.timedelta(seconds=61)
        self.assertEqual(View._strfdelta(tdelta), "1:01")
