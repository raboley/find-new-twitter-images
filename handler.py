#import tweepy
import json
import os
from twython import Twython
import configparser

call = os.system
config_path = './config.cfg'
# def authorize_config():
#     authorise_twitter_api(config)

# def get_api():
#     return tweepy.API(auth, wait_on_rate_limit=True)

# def get_tweets(api, username, include_rts, exclude_replies):
#     status = tweepy.Cursor(api.user_timeline, screen_name=username, include_rts=include_rts, exclude_replies=exclude_replies, tweet_mode='extended').items()

def hello(event, context):
    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }
    call("python download_twitter_photos.py --username cloud_images --num 10 --replies --retweets --output delivered --bucket dark-cloud-bucket2")
    return response

    # Use this code if you don't use the http event with the LAMBDA-PROXY
    # integration
    """
    return {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event
    }
    """

def parse_config(config_file):
  config = configparser.ConfigParser()
  config.read(config_file)
  return config 


def main():
    config = parse_config(config_path)
    get_tweepy_access(config)

def get_tweepy_access(config):
    APP_KEY = config['DEFAULT']['consumer_key']
    APP_SECRET = config['DEFAULT']['consumer_secret']

    twitter = Twython(APP_KEY, APP_SECRET, oauth_version=2)
    ACCESS_TOKEN = twitter.obtain_access_token()

if __name__=='__main__':
    main()

