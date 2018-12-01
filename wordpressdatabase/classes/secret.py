from json import loads
from logging import error, getLogger, info

from boto3 import client
from boto3.session import Session

from wordpressdatabase.exceptions import RegionNotKnownError

class Secret():

    def __init__(self, identifier, region=None):
        self._client = None
        self._identifier = identifier
        self._region = region
        self._secret_string = None

    @property
    def region(self):
        """
        Get the AWS region.

        Raises:
            RegionNotKnownError: Raised when the AWS region was not specified
                                    and could not be determined.

        Returns:
            str: AWS region.
        """

        if self._region:
            return self._region

        info('Looking up the current session\'s region...')

        self._region = Session().region_name

        if self._region:
            info('Current session is in %s.', self._region)
            return self._region

        error('Session does not describe a region.')

        raise RegionNotKnownError()

    @property
    def as_string(self):
        if self._secret_string:
            return self._secret_string

        if not self._client:
            self._client = client('secretsmanager',
                                  region_name=self.region)

        response = self._client.get_secret_value(SecretId=self._identifier)
        self._secret_string = response['SecretString']
        return self._secret_string

    @property
    def as_dict(self):
        return loads(self.as_string)
