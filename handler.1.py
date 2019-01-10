import download_twitter_photos
import os

call = os.system

# python download_twitter_photos.py --username cloud_images --num 10 --replies --retweets --output delivered --bucket dark-cloud-bucket2
def handler(event,context):
    """downloads photos from a twitter handle"""
    print("I am here! " + context.functionName  +  ":"  +  context.functionVersion)
    call("python download_twitter_photos.py --username cloud_images --num 10 --replies --retweets --output delivered --bucket dark-cloud-bucket2")
    print('Finished:' + context.functionName  +  ":"  +  context.functionVersion)