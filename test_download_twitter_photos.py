import unittest
import download_twitter_photos

dl = download_twitter_photos

class test_get_already_downloaded(unittest.TestCase):
    """
    Ensure get_already_downloaded returns a set of file names
    """
    def setUp(self):
        self.test_list = ['DuvaqaUUcAEJFwm.jpg', 'DuyDTUaXgAMN_dk.jpg','DvO94MtUwAEvIEJ.jpg','DvO94PpU0AAnNa1.jpg','DwGfVKQU8AEHvbf.jpg']
    
    @unittest.skip("Not a good test, calls the api to read s3 and check in hardcoded value")
    def test_returns_an_object_of_file_names(self):
        l = dl.get_already_downloaded(bucket='dark-cloud-bucket', prefix='archive/')
        self.assertIn('DuvaqaUUcAEJFwm.jpg', l)

    def test_returns_filename_without_full_path(self):
        l = dl.get_already_downloaded(bucket='dark-cloud-bucket', prefix='archive/')
        for i in l:
            self.assertNotRegex(i, '\\\\')

    def test_returns_true_when_object_is_NOT_array(self):
        self.assertTrue(dl.image_is_new('not.jpg',self.test_list))

    def test_returns_false_when_object_is_in_array(self):
        self.assertFalse(dl.image_is_new('DuvaqaUUcAEJFwm.jpg',self.test_list))
    
    def test_returns_true_if_hashtag_in_event_string(self):
        string = '#DarkCloudRocks'
        self.assertTrue(dl.has_hashtag(string))
        
    def test_returns_false_if_hashtag_not_in_event_string(self):
        string = 'cloud_images'
        self.assertFalse(dl.has_hashtag(string))

if __name__ == '__main__':
    unittest.main()