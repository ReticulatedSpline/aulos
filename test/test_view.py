import datetime
import unittest
import typing

from src.view import View, Display, DisplayItem, ItemType


class TestViewMethods(unittest.TestCase):

    def test_strfdelta(self):
        tdelta = None
        self.assertEqual(View._strfdelta(tdelta), "-:--")
        tdelta = datetime.timedelta(seconds=0)
        self.assertEqual(View._strfdelta(tdelta), "0:00")
        tdelta = datetime.timedelta(seconds=10)
        self.assertEqual(View._strfdelta(tdelta), "0:10")
        tdelta = datetime.timedelta(minutes=1, seconds=30)
        self.assertEqual(View._strfdelta(tdelta), "1:30")
        tdelta = datetime.timedelta(seconds=61)
        self.assertEqual(View._strfdelta(tdelta), "1:01")
        tdelta = datetime.timedelta(days=1, hours=1, minutes=1, seconds=1)
        self.assertEqual(View._strfdelta(tdelta), "1d, 1h, 1:01")
        tdelta = datetime.timedelta(days=15, hours=26, minutes=9, seconds=1)
        self.assertEqual(View._strfdelta(tdelta), "16d, 2h, 9:01")

    def test_truncate_string(self):
        self.assertEqual("", View._truncate_string(None, 0))
        empty_str = ""
        self.assertEqual("", View._truncate_string(empty_str, 10))
        short_str = "should fit"
        self.assertEqual("should fit", View._truncate_string(short_str, 15))
        long_str = "this will need to be truncated to fit into 16 characters!"
        expected_str = "...6 characters!"
        self.assertEqual(expected_str, View._truncate_string(long_str, 16))

    def test_draw_progress_bar(self):
        self.assertEqual(None, View._draw_progress_bar(0, 0, 0))
        self.assertEqual(None, View._draw_progress_bar(-1, -1, -1))
        
        expected_str = "▒▒▒▒▒▒▒▒▒▒"
        returned_str = View._draw_progress_bar(0, 0, 10)
        self.assertEqual(expected_str, returned_str)
        
        expected_str = "█████▒▒▒▒▒"
        returned_str = View._draw_progress_bar(10, 5, 10)
        self.assertEqual(expected_str, returned_str)
        
        expected_str = "██████████"
        returned_str = View._draw_progress_bar(10, 10, 10)
        self.assertEqual(expected_str, returned_str)
        returned_str = View._draw_progress_bar(5, 10, 10)
        self.assertEqual(expected_str, returned_str)