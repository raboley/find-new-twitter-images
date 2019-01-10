import tweepy
import os
from tweepy import OAuthHandler
import json
import argparse
import configparser
from boto3 import client as boto3_client
from datetime import datetime

lambda_client = boto3_client('lambda')

## Getting tweets and downloading are now linked
# TODO: make the function to get everything in the s3 bucket so we don't download twice
# TODO: compare that list vs the item to determine if we should download it or not
# TODO: set up the handler to call this function
# TODO: make sure to give this function permissions to call other functions

"""
   {
        "Sid": "Stmt1234567890",
        "Effect": "Allow",
        "Action": [
            "lambda:InvokeFunction"
        ],
        "Resource": "*"
    }
"""

def parse_config(config_file):
  config = configparser.ConfigParser()
  config.read(config_file)
  return config 
  
@classmethod
def parse(cls, api, raw):
    status = cls.first_parse(api, raw)
    setattr(status, 'json', json.dumps(raw))
    return status

def init_tweepy():
  # Status() is the data model for a tweet
  tweepy.models.Status.first_parse = tweepy.models.Status.parse
  tweepy.models.Status.parse = parse
  # User() is the data model for a user profil
  tweepy.models.User.first_parse = tweepy.models.User.parse
  tweepy.models.User.parse = parse

def authorize_twitter_api(config):
  auth = OAuthHandler(config['DEFAULT']['consumer_key'], config['DEFAULT']['consumer_secret'])
  auth.set_access_token(config['DEFAULT']['access_token'], config['DEFAULT']['access_secret'])
  return auth

# It returns [] if the tweet doesn't have any media
def tweet_media_urls(tweet_status):
  media = tweet_status._json.get('extended_entities', {}).get('media', [])
  if (len(media) == 0):
    return []
  else:
    return [item['media_url'] for item in media]

def get_tweets(api, screen_name, include_rts, exclude_replies):
  return tweepy.Cursor(api.user_timeline, screen_name=screen_name, include_rts=include_rts, exclude_replies=exclude_replies, tweet_mode='extended').items()

def determine_new_tweets(status, num_tweets, output_folder):
  downloaded = 0

  for tweet_status in status:

    if(downloaded >= num_tweets):
      break

    for media_url in tweet_media_urls(tweet_status):
      # Only download if there is not a picture with the same name in the folder already
      file_name = os.path.split(media_url)[1]
      if image_is_new(media_url): #os.path.exists(os.path.join(output_folder, file_name)):
        print(media_url)
        download_path = 'archive/' + file_name
        tell_lambda_to_download_image(media_url=media_url, download_path=download_path)
        downloaded += 1

def image_is_new(media_url):
  already_downloaded = get_already_downloaded()
  return True

def get_already_downloaded():
  pass

def add_url_to_response(media_url):
  pass

def tell_lambda_to_download_image(media_url, download_path):
    msg = { 
      "image_url": media_url,
      "key": download_path
      }
    invoke_response = lambda_client.invoke(FunctionName="fetch-file-and-store-in-s3-dark-cloud-dev-save",
                                           InvocationType='Event',
                                           Payload=json.dumps(msg))
    print(invoke_response)

def get_arguments():
  args = { 
    'config': './config.cfg',
    'username': 'cloud_images',
    'hashtag': '',
    'num': 5,
    'retweets': False,
    'replies': False,
    'output': 'pictures/',
    'bucket': 'dark-cloud-bucket'
  }
  return args

def main():
  arguments = get_arguments() 
  username = arguments['username']
  hashtag = arguments['hashtag']
  retweets = arguments['retweets']
  replies = arguments['replies']
  num_tweets = arguments['num']
  output_folder = arguments['output']
  config_path = arguments['config']
  bucket = arguments['bucket']

  config = parse_config(config_path)
  auth = authorize_twitter_api(config)
  api = tweepy.API(auth, wait_on_rate_limit=True)

  tweets = get_tweets(api, retweets, replies, num_tweets)
  determine_new_tweets(status=tweets, num_tweets=num_tweets, output_folder=output_folder)
  
#  if hashtag:
#    download_images_by_tag(api, hashtag, retweets, replies, num_tweets, output_folder, bucket)
#  else:
#    download_images_by_user(api, username, retweets, replies, num_tweets, output_folder, bucket)

if __name__=='__main__':
    main()
