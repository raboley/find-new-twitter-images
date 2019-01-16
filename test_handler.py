import unittest
import handler


class test_handler(unittest.TestCase):
    """
    Ensure that new tweets get downloaded to s3 when called with valid arguments
    """

    def setUp(self):
        self.default_event = {
            "config": "./config.cfg",
            "username_or_hashtag": "cloud_images",
            "hashtag": "",
            "num": "3",
            "retweets": "False",
            "replies": "False",
            "output_folder": "__testing/",
            "bucket": "dark-cloud-bucket",
            "download_lambda_name": "fetch-file-and-store-in-s3-dark-cloud-dev-save"
        }

    def test_parse_event_returns_default_values_if_nothing_passed_in(self):
        event = ""
        output_event = handler.parse_event(self.default_event,event)
        self.assertDictEqual(self.default_event, output_event)

    def test_parse_event_updates_entry_if_one_parameter_is_passed_in(self):
        event = { "output_folder": "__testing2/" }
        expected_event = {
            "config": "./config.cfg",
            "username_or_hashtag": "cloud_images",
            "hashtag": "",
            "num": "3",
            "retweets": "False",
            "replies": "False",
            "output_folder": "__testing2/",
            "bucket": "dark-cloud-bucket",
            "download_lambda_name": "fetch-file-and-store-in-s3-dark-cloud-dev-save"
        }
        output_event = handler.parse_event(self.default_event,event)
        self.assertDictEqual(expected_event, output_event)
    
    def test_parse_event_all_fields_passed_in_update_correctly(self):
        event = {
            "config": "./config2.cfg",
            "username_or_hashtag": "cloud_i124mages",
            "hashtag": "325",
            "num": "33",
            "retweets": "True",
            "replies": "True",
            "output_folder": "__dtesting2/",
            "bucket": "dark-cloud-bucket2",
            "download_lambda_name": "fetch-file-and-store-in-s3-dark-cloud-dev-savsafe"
        }
        expected_event = {
            "config": "./config2.cfg",
            "username_or_hashtag": "cloud_i124mages",
            "hashtag": "325",
            "num": "33",
            "retweets": "True",
            "replies": "True",
            "output_folder": "__dtesting2/",
            "bucket": "dark-cloud-bucket2",
            "download_lambda_name": "fetch-file-and-store-in-s3-dark-cloud-dev-savsafe"
        }
        output_event = handler.parse_event(self.default_event,event)
        self.assertDictEqual(expected_event, output_event)