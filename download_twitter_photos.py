from twitter import Twitter, TwitterHashTag
import os
from tweepy import OAuthHandler
import json
import argparse
import configparser
from boto3 import client as boto3_client
from datetime import datetime
import get_matching_s3_objects

lambda_client = boto3_client('lambda')
get3 = get_matching_s3_objects.get_matching_s3_keys


def download_new_images(media_urls, num_tweets, output_folder, list_of_downloaded_images, bucket, download_lambda_name):
  downloads = []
  if media_urls:
    for media_url in media_urls:
      # Only download if there is not a picture with the same name in the folder already
      file_name = os.path.split(media_url)[1]
      if image_is_new(file_name=file_name, list_of_downloaded_images=list_of_downloaded_images):
        print("downloading: "+ media_url)
        
        download_path = output_folder + file_name
        
        tell_lambda_to_download_image(media_url=media_url, download_path=download_path, bucket=bucket, download_lambda_name=download_lambda_name)
        msg = {
          "bucket": bucket,
          "output_folder": output_folder,
          "file_name": file_name,
          "download_path": download_path,
          "lambda_invoked": download_lambda_name
        }
        downloads.append(json.dumps(msg))
  return downloads


def image_is_new(file_name, list_of_downloaded_images):
  if file_name in list_of_downloaded_images:
    return False
  else:
    return True

def get_already_downloaded(bucket, prefix='', suffix=''):
  file_names = []
  fullpaths = get3(bucket=bucket, prefix=prefix, suffix=suffix)
  for fullpath in fullpaths:
    file_name = os.path.split(fullpath)[1]
    file_names.append(file_name) 
  return file_names

def add_url_to_response(media_url):
  pass

def tell_lambda_to_download_image(media_url, download_path, bucket, download_lambda_name):
    msg = { 
      "image_url": media_url,
      "key": download_path,
      "bucket": bucket
      }
    invoke_response = lambda_client.invoke(FunctionName=download_lambda_name,
                                           InvocationType='Event',
                                           Payload=json.dumps(msg))
    print(invoke_response)

def has_hashtag(string):
  return True if '#' in string else False

def main(arguments):
  username_or_hashtag = arguments['username_or_hashtag']
  #hashtag = arguments['hashtag']
  include_rts = arguments['retweets']
  exclude_replies = arguments['replies']
  num_tweets = int(arguments['num'])
  output_folder = arguments['output_folder']
  config_path = arguments['config']
  bucket = arguments['bucket']
  download_lambda_name = arguments['download_lambda_name']
  
  if has_hashtag(username_or_hashtag):
    twitter = TwitterHashTag(config_path)
  else:
    twitter = Twitter(config_path)

  list_of_downloaded_images = get_already_downloaded(bucket=bucket, prefix=output_folder, suffix='')
  media_urls = twitter.get_tweet_media_urls(username_or_hashtag, include_rts=include_rts, exclude_replies=exclude_replies,max_number_image_urls=num_tweets)
  return download_new_images(media_urls=media_urls, num_tweets=num_tweets, output_folder=output_folder, list_of_downloaded_images=list_of_downloaded_images, bucket=bucket, download_lambda_name=download_lambda_name)

if __name__=='__main__':
    event = {
        "config": "./config.cfg",
        "username_or_hashtag": "cloud_images",
        "hashtag": "",
        "num": "3",
        "retweets": "False",
        "replies": "False",
        "output_folder": "archive/",
        "bucket": "dark-cloud-bucket",
        "download_lambda_name": "fetch-file-and-store-in-s3-dark-cloud-dev-save"
    }
    main(event)
