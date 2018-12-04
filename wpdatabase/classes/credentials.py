""" Database credentials. """

from wpdatabase.classes import Secret
from wpdatabase.exceptions import InvalidArgumentsError


class Credentials():
    """
    Represents a set of database credentials.

    You should consider using either the 'from_aws_secrets_manager' or
    'from_username_and_password' static functions rather than this constructor.

    If you must use the constructor, then pass only:

     - A username and a password, or:
     - An Amazon Web Services (AWS) Secrets Manager secret ID and a region.

    Args:
        username (str, optional):      Username.
        password (str, optional):      Password.
        aws_secret_id (str, optional): Amazon Web Services (AWS) Secrets
                                       Manager secret ID to extract the
                                       credentials from.
        region (str, optional):        AWS region where the secret resides.

    Raises:
        InvalidArgumentsError:         An invalid combination of arguments was
                                       passed to the constructor.
    """

    def __init__(self,
                 username=None,
                 password=None,
                 aws_secret_id=None,
                 region=None):

        if (not username) != (not password):
            raise InvalidArgumentsError(
                'Must specify both the username and password or neither.')

        if (not username) == (not aws_secret_id):
            raise InvalidArgumentsError(
                'Must specify the username or the secret identifier.')

        self._username = username
        self._password = password

        if aws_secret_id:
            self._secret = Secret(identifier=aws_secret_id, region=region)
        else:
            self._secret = None

    def _resolve_secret(self):
        if not self._secret:
            return
        self._username = self._secret.as_dict['username']
        self._password = self._secret.as_dict['password']
        self._secret = None

    @staticmethod
    def from_aws_secrets_manager(secret_id, region):
        """
        Gets a Credentials instance by extracting the username and password
        from Amazon Web Services (AWS) Secrets Manager.

        Args:
            secret_id (str): Secret ID.
            region (str):    AWS region where the secret resides.

        Returns:
            Credentials:     Credentials instance.
        """
        return Credentials(aws_secret_id=secret_id, region=region)

    @staticmethod
    def from_username_and_password(username, password):
        """
        Gets a Credentials instance by populating it directly with a known
        username and password.

        Args:
            username (str): Username.
            password (str): Password.

        Returns:
            Credentials:    Credentials instance.
        """
        return Credentials(username=username, password=password)

    @property
    def username(self):
        """ Gets the username. """
        self._resolve_secret()
        return self._username

    @property
    def password(self):
        """ Gets the password. """
        self._resolve_secret()
        return self._password
