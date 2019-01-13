import unittest
import twitter

class test_Twitter(unittest.TestCase):
    """
    Ensure that new tweets get downloaded to s3 when called with valid arguments
    """

    def setUp(self):
        self.twitter = twitter.Twitter('./config.cfg')
    
    def test_returns_list_of_media_url_strings(self):
        media_urls = self.twitter.get_tweet_media_urls(screen_name='cloud_images',include_rts=False,exclude_replies=True)
        self.assertTrue(media_urls)
    
    def test_returns_specified_number_of_tweets(self):
        max_to_return = 2
        media_urls = self.twitter.get_tweet_media_urls(screen_name='cloud_images',include_rts=False,exclude_replies=True, max_number_image_urls=max_to_return)
        self.assertEqual(max_to_return, media_urls.__len__()) 