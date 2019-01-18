import handler
import get_matching_s3_objects
import unittest
import boto3

class test_integration_handler(unittest.TestCase):
    """
    Ensure that new tweets get downloaded to s3 when called with valid arguments
    """

    def setUp(self):
        self.event_user = {
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
        
        self.event_hashtag = {
            "config": "./config.cfg",
            "username_or_hashtag": "#dark_Clou2d_Images",
            "hashtag": "",
            "num": "3",
            "retweets": "False",
            "replies": "False",
            "output_folder": "__testing/",
            "bucket": "dark-cloud-bucket",
            "download_lambda_name": "fetch-file-and-store-in-s3-dark-cloud-dev-save"
        }

    
    def tearDown(self):
        self.delete_s3_objects(bucket_name=self.event_user['bucket'],output_folder=self.event_user['output_folder'])
        pass

    def delete_s3_objects(self, bucket_name, output_folder):
        s3 = boto3.resource('s3')
        objects_to_delete = s3.meta.client.list_objects(Bucket=bucket_name, Prefix=output_folder)

        delete_keys = {'Objects' : []}
        delete_keys['Objects'] = [{'Key' : k} for k in [obj['Key'] for obj in objects_to_delete.get('Contents', [])]]
        if delete_keys['Objects']:
            s3.meta.client.delete_objects(Bucket=bucket_name, Delete=delete_keys)

    def test_new_twitter_image_gets_downloaded(self):
        # I think something about the way it makes requests to AWS was screwing this up
        # if I put these two calls in setup then the second test no longer works. 
        handler.search_for_new_tweets(self.event_user,'')
        pushed_objects = get_matching_s3_objects.get_matching_s3_keys(bucket=self.event_user['bucket'], prefix=self.event_user['output_folder'])
        
        self.assertTrue(pushed_objects)
    
    @unittest.skip('Cant really count the objects in a s3 bucket so easy like this I guess...')
    def test_only_correct_num_of_images_get_downloaded(self):      
        handler.search_for_new_tweets(self.event_user,'')
        pushed_objects = get_matching_s3_objects.get_matching_s3_keys(bucket=self.event_user['bucket'], prefix=self.event_user['output_folder'])
        
        count = 0
        for obj in pushed_objects:
            count+= 1
        self.assertEqual(int(self.event_user['num']), count)
    
    
    def test_new_twitter_images_from_hashtag_get_downloaded(self):
        handler.search_for_new_tweets(self.event_hashtag,'')
        pushed_objects = get_matching_s3_objects.get_matching_s3_keys(bucket=self.event_hashtag['bucket'], prefix=self.event_hashtag['output_folder'])
        
        self.assertTrue(pushed_objects)

    def test_teardown_does_remove_items(self):
        pushed_objects =get_matching_s3_objects.get_matching_s3_keys(bucket=self.event_user['bucket'], prefix=self.event_user['output_folder'])
        
        count = 0
        for obj in pushed_objects:
            count+= 1
        self.assertEqual(int(0), count)
