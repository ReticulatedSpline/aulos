import datetime
import unittest
import typing

from src.view import View, Display, DisplayItem, ItemType


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

    def test_truncate_string(self):
        empty_str = ""
        self.assertEqual("", View._truncate_string(empty_str, 10))
        short_str = "should fit"
        self.assertEqual("should fit", View._truncate_string(short_str, 15))
        
