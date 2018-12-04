""" A secret from Amazon Web Services Secrets Manager. """


import json
import logging

import boto3

from wpdatabase.exceptions import RegionNotKnownError


class Secret():
    """
    A secret from Amazon Web Services Secrets Manager.

    Args:
        identifier (str):          Secret ID.
        region (region, optional): AWS region in which the secret resides.
    """

    def __init__(self, identifier, region=None):
        self._client = None
        self._identifier = identifier
        self._log = logging.getLogger(__name__)
        self._region = region
        self._secret_string = None

    @property
    def region(self):
        """
        Gets the AWS region.

        Raises:
            RegionNotKnownError: Raised when the AWS region was not specified
                                 and could not be determined.

        Returns:
            str: AWS region.
        """

        if self._region:
            return self._region

        self._log.info('Looking up the current session\'s region...')
        self._region = boto3.session.Session().region_name

        if self._region:
            self._log.info('Current session is in %s.', self._region)
            return self._region

        self._log.critical('Session does not describe a region.')
        raise RegionNotKnownError()

    @property
    def as_string(self):
        """
        Gets the secret value as a string.

        Returns:
            str: Secret value.
        """

        if self._secret_string:
            return self._secret_string

        self._log.info('Creating secretsmanager client...')

        if not self._client:
            self._client = boto3.client('secretsmanager',
                                        region_name=self.region)

        self._log.info('Downloading secret value...')
        response = self._client.get_secret_value(SecretId=self._identifier)
        self._secret_string = response['SecretString']
        self._log.info('Downloaded secret value.')
        return self._secret_string

    @property
    def as_dict(self):
        """
        Gets the secret value as JSON-deserialized dictionary.

        Returns:
            dict: Secret value.
        """
        return json.loads(self.as_string)
