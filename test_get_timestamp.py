from get_timestamp import get_datetime_no_spaces
import unittest
from unittest.mock import patch


class test_get_datetime_no_spaces(unittest.TestCase):
    """
    Ensure we get a datetimestamp that will work for our archive folder path
    """
    @patch('get_timestamp.get_datetime_no_spaces', return_value='pumpkins')

    def test_replaces_spaces_with_underscores(self):
        string = get_datetime_no_spaces()
        self.assertEqual(-1,string.find(" "))

    def test_replaces_colons_with_dashes(self):
        string = get_datetime_no_spaces()
        self.assertEqual(-1,string.find(":"))

    def test_removes_everthing_after_the_period(self):
        string = get_datetime_no_spaces()
        self.assertEqual(19,string.__len__())