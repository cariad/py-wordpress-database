""" An invalid database name was encountered. """


class InvalidDatabaseNameError(Exception):
    """
    An invalid database name was encountered.

    Args:
        name (str): The invalid database name.
    """

    def __init__(self, name):
        message = '"{}" is not a valid database name.'.format(name)
        super().__init__(message)
