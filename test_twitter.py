import unittest
import twitter

class test_Twitter(unittest.TestCase):
    """
    Ensure that a list of tweet media urls are returned
    """

    def setUp(self):
        self.twitter = twitter.Twitter('./config.cfg')
    
    @unittest.skip('cant test internal methods without constructing thing first')
    def test_config_returns_all_keys_and_secrets(self):
        config = twitter.Twitter._Twitter__parse_config(config_file='./config.cfg')
        self.assertTrue(config['DEFAULT']['consumer_key'])
        self.assertTrue(config['DEFAULT']['consumer_secret'])
        self.assertTrue(config['DEFAULT']['access_token'])
        self.assertTrue(config['DEFAULT']['access_secret'])

    @unittest.skip('cant test internal methods without constructing thing first')
    def test_auth_correctly_gets_authorization(self):
        config = twitter.Twitter._Twitter__parse_config(config_file='./config.cfg')
        auth = twitter.Twitter._Twitter__authorize_twitter_api(config)
        self.assertTrue(auth)


    def test_returns_list_of_media_url_strings(self):
        media_urls = self.twitter.get_tweet_media_urls(screen_name='cloud_images',include_rts=False,exclude_replies=True)
        self.assertTrue(media_urls)
    
    def test_returns_two_photo_urls(self):
        max_to_return = 2
        media_urls = self.twitter.get_tweet_media_urls(screen_name='cloud_images',include_rts=False,exclude_replies=True, max_number_image_urls=max_to_return)
        self.assertEqual(max_to_return, media_urls.__len__()) 

    def test_returns_three_photo_urls(self):
        max_to_return = 3
        media_urls = self.twitter.get_tweet_media_urls(screen_name='cloud_images',include_rts=False,exclude_replies=True, max_number_image_urls=max_to_return)
        self.assertEqual(max_to_return, media_urls.__len__()) 