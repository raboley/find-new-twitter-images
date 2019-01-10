import unittest
import os

call = os.system

class test_requirements_are_installed_and_configured(unittest.TestCase):
    """
    Ensure that all required modules are installed in this context
    """
    def test_pip_is_installed(self):
        self.assertEqual(call("pip -help"),0)
    
    def test_virtual_env_is_installed(self):
        self.assertEqual(call("virtualenv --version"),0)

    def test_boto3_is_installed(self):
        self.assertEqual(call("pip freeze | grep boto3"),0)

    def test_aws_cli_is_installed(self):
        self.assertEqual(call("aws --version"),0)

    def test_aws_credentials_and_keys_configured(self):
        self.assertEqual(call("aws iam list-users"),0)

    def test_tweepy_is_installed(self):
        self.assertEqual(call("pip freeze | grep tweepy"),0)