""" Tests for the Credentials class. """

import unittest

from wpdatabase.classes import Credentials


class CredentialsTestCase(unittest.TestCase):
    """ Tests for the Credentials class. """

    def test_from_aws_secrets_manager(self):
        """
        Assert that from_aws_secrets_manager() returns a class instance.
        """

        instance = Credentials.from_aws_secrets_manager(
            secret_id='my-secret-id',
            region='my-region')

        self.assertTrue(isinstance(instance, Credentials))

    def test_from_username_and_password(self):
        """
        Assert that from_username_and_password() returns a class instance.
        """

        instance = Credentials.from_username_and_password(
            username='username',
            password='password')

        self.assertTrue(isinstance(instance, Credentials))


if __name__ == '__main__':
    unittest.main()
