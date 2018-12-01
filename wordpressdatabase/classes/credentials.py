""" Database credentials. """

from wordpressdatabase.classes import Secret
from wordpressdatabase.exceptions import InvalidParametersError


class Credentials():

    def __init__(self,
                 username=None,
                 password=None,
                 secret_id=None,
                 region=None):

        if (not username) != (not password):
            raise InvalidParametersError(
                'Must specify both the username and password or neither.')

        if (not username) == (not secret_id):
            raise InvalidParametersError(
                'Must specify the username or the secret identifier.')

        self._username = username
        self._password = password

        if secret_id:
            self._secret = Secret(identifier=secret_id, region=region)
        else:
            self._secret = None

    def resolve_secret(self):
        if not self._secret:
            return

        self._username = self._secret.as_dict['username']
        self._password = self._secret.as_dict['password']
        self._secret = None

    @property
    def username(self):
        self.resolve_secret()
        return self._username

    @property
    def password(self):
        self.resolve_secret()
        return self._password
