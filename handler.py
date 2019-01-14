import json
import download_twitter_photos


def search_for_new_tweets(event, context):
    output = download_twitter_photos.main(arguments=event)
    
    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event,
        "output": output
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }
    return response

# Use this code if you don't use the http event with the LAMBDA-PROXY
# integration
"""
return {
    "message": "Go Serverless v1.0! Your function executed successfully!",
    "event": event
}
"""

# def get_arguments(username='cloud_images', destination_bucket='dark-cloud-bucket', num=5, output_folder='archive/', download_lambda_name='fetch-file-and-store-in-s3-dark-cloud-dev-save'):
#   args = { 
#     'config': './config.cfg',
#     'username': username,
#     'hashtag': '',
#     'num': num,
#     'retweets': False,
#     'replies': False,
#     'output_folder': output_folder,
#     'bucket': destination_bucket,
#     'download_lambda_name': download_lambda_name
#   }
#   print(args)
#   return args

if __name__ == '__main__':
    #get_arguments()
    event = {
        "config": "./config.cfg",
        "username_or_hashtag": "cloud_images",
        "hashtag": "",
        "num": "5",
        "retweets": "False",
        "replies": "False",
        "output_folder": "archive/",
        "bucket": "dark-cloud-bucket",
        "download_lambda_name": "fetch-file-and-store-in-s3-dark-cloud-dev-save"
    }
    search_for_new_tweets(event,'')