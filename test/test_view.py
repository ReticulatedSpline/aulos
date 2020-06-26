import os
import sys
import unittest
from datetime import timedelta
from view import View


class TestViewMethods(unittest.TestCase):

    def setUp(self):
        self.view = View()

    def test_strfdelta(self):
        self.assertEqual(self.view.timedelta(seconds=10), 'FOO')


if __name__ == '__main__':
    unittest.main()
