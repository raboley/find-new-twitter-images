import tweepy
from tweepy import OAuthHandler
import json
import configparser

class Twitter:
    """
    Class that connects to twitter API and returns urls to the media (images) in tweets

    ...

    Attributes
    ----------
    api : 
        The authenticated connection to twitter from which api calls are made.

    Methods
    -------
    get_tweet_media_urls
        returns n number of tweet media urls from a specified user
    """

    def __parse_config(self, config_file):
        config = configparser.ConfigParser()
        config.read(config_file)
        return config 
    
    def __authorize_twitter_api(self, config):
        auth = OAuthHandler(config['DEFAULT']['consumer_key'], config['DEFAULT']['consumer_secret'])
        auth.set_access_token(config['DEFAULT']['access_token'], config['DEFAULT']['access_secret'])
        return auth

    # It returns [] if the tweet doesn't have any media
    def extract_media_url(self, tweet_status, max_number_image_urls):   
        """Extracts the full url to the media in a tweet
        
        Parameters
        ----------
        tweet_status : [type]
            The raw feed of tweets returned from a tweepy.Cursor
        max_number_image_urls : [type]
            The max number of image urls that should be returned, less than 100
        
        Returns
        -------
        list
            list of urls pointing to media from tweets
        """

        if not tweet_status:
            return []
        
        media_urls =[]
        url_count = 0        

        for tweet in tweet_status:
            media = tweet._json.get('extended_entities', {}).get('media', [])
            if (len(media) == 0):
                continue
            else:
                for item in media:
            
                    if url_count >= max_number_image_urls:
                        break

                    media_urls.append(item['media_url'])
                    url_count += 1
        return media_urls

    def get_tweet_media_urls(self, screen_name, include_rts, exclude_replies,max_number_image_urls=100):
        """Gets the full url to the media of a tweet stream by username.

        Parameters
        ----------
        screen_name : str
            The twitter username to search by without the @ symbol.
                Ex. twitter user @cloud_images would be passed in as cloud_images
        include_rts : bool
            A flag to determine if you want to also get media from things the user retweeted
        exclude_replies : bool
            A flag to determine if you want to exclude replies the user made to others
        max_number_image_urls : int
            The maximum number of image urls to get. The max is 100,
            but if there are fewer urls than 100 it will return as
            many as there are.

        Returns
        -------
        list
            a list of strings representing the full url to the media behind a tweet (ex. image url)
        """
        
        raw_tweets = tweepy.Cursor(self.api.user_timeline, screen_name=screen_name, include_rts=include_rts, exclude_replies=exclude_replies, tweet_mode='extended').items()
        tweet_media_urls = self.extract_media_url(tweet_status=raw_tweets,max_number_image_urls=max_number_image_urls)
        return tweet_media_urls

    def __init__(self, config_path):
        """init a twitter object that creates a connection based on API keys in a config file
        
        Parameters
        ----------
        config_path : str
            the path to a config file holding the API keys to use the twitter API. ex ./config.cfg
        
        """
        config = self.__parse_config(config_file=config_path)
        auth = self.__authorize_twitter_api(config)
        self.api = tweepy.API(auth_handler=auth, wait_on_rate_limit=True)


class TwitterHashTag(Twitter):

    def get_tweet_media_urls(self, search_string, include_rts, exclude_replies, max_number_image_urls=100):
        """Gets the full url to the media of a tweet stream by hashtag.

        Parameters
        ----------
        search_string : str
            the hashtag to search by including the `#` symbol
                Ex. to get all tweets from trend #cloud_rocks the string `#cloud_rocks` would be passed
        include_rts : bool
            A flag to determine if you want to also get media from things the user retweeted
        exclude_replies : bool
            A flag to determine if you want to exclude replies the user made to others
        max_number_image_urls : int
            The maximum number of image urls to get. The max is 100,
            but if there are fewer urls than 100 it will return as
            many as there are.

        Returns
        -------
        list
            a list of strings representing the full url to the media behind a tweet (ex. image url)
        """
        raw_tweets = tweepy.Cursor(self.api.search, search_string, include_rts=include_rts, exclude_replies=exclude_replies, tweet_mode='extended').items()
        tweet_media_urls = self.extract_media_url(tweet_status=raw_tweets,max_number_image_urls=max_number_image_urls)
        return tweet_media_urls
    
    