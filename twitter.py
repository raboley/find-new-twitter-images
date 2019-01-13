import tweepy
from tweepy import OAuthHandler
import json
import configparser

class Twitter:

    def get_tweet_media_urls(self, screen_name, include_rts, exclude_replies,max_number_image_urls=100):
        raw_tweets = tweepy.Cursor(self.api.user_timeline, screen_name=screen_name, include_rts=include_rts, exclude_replies=exclude_replies, tweet_mode='extended').items()
        tweet_media_urls = self.__extract_media_url(tweet_status=raw_tweets,max_number_image_urls=max_number_image_urls)
        return tweet_media_urls

    # It returns [] if the tweet doesn't have any media
    def __extract_media_url(self, tweet_status, max_number_image_urls):   
        for tweet in tweet_status:
            media = tweet._json.get('extended_entities', {}).get('media', [])
            if (len(media) == 0):
                return []
            else:
                url_count = 0
                media_urls =[]
                
                for item in media:
                    
                    if url_count >= max_number_image_urls:
                        break

                    media_urls.append(item['media_url'])
                    url_count += 1
                return media_urls

    def __init__(self, config_path):
        config = self.__parse_config(config_file=config_path)
        auth = self.__authorize_twitter_api(config)
        self.api = tweepy.API(auth_handler=auth, wait_on_rate_limit=True)
    

    def __parse_config(self, config_file):
        config = configparser.ConfigParser()
        config.read(config_file)
        return config 
    
    def __authorize_twitter_api(self, config):
        auth = OAuthHandler(config['DEFAULT']['consumer_key'], config['DEFAULT']['consumer_secret'])
        auth.set_access_token(config['DEFAULT']['access_token'], config['DEFAULT']['access_secret'])
        return auth

