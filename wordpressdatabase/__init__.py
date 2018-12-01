"""
"wordpressdatabase" package initialization.
"""

import json
from logging import getLogger

import boto3

from mysql import connector
from wpconfigr import WpConfigFile

from wordpressdatabase.classes import Database
from wordpressdatabase.exceptions import InvalidDatabaseNameError


LOG = getLogger(__name__)


def update_wp_config(wp_config, host, db_name, user_credentials, port=None):
    """
    Update the WordPress configuration to match the requested values.

    Args:
        wp_config (WpConfigFile): Configuration.
        host (str): Database hostname.
        db_name (str): Database name.
        user_credentials (Credentials): WordPress database user credentials.
        port (str, optional): Database port.

    Raises:
        Exception: [description]
    """

    LOG.info('Updating WordPress configuration...')

    for char in db_name:
        if str.isalnum(char) or char == '_':
            continue

        LOG.error('"%s" is not valid in a database name.', char)
        raise InvalidDatabaseNameError(db_name)

    if port:
        host_and_port = host + ':' + port
    else:
        host_and_port = host

    wp_config.set('DB_HOST', host_and_port)
    wp_config.set('DB_USER', user_credentials.username)
    wp_config.set('DB_PASSWORD', user_credentials.password)
    wp_config.set('DB_NAME', db_name)


def ensure(wp_config_filename,
           admin_credentials,
           user_credentials,
           host,
           db_name,
           port=None):
    """
    Ensures that the WordPress configuration matches the specified values and
    that the database is set up.

    Args:
        wp_config_filename (str):        Path and filename of "wp-config.php".
        admin_credentials (Credentials): Database admin user credentials.
        user_credentials (Credentials):  WordPress database user credentials.
        host (str):                      Database host.
        db_name (str):                   Database name.
        port (int, optional):            Database port.

    Raises:
        InvalidDatabaseNameError: The database name is invalid.
    """

    wp_config = WpConfigFile(filename=wp_config_filename)

    update_wp_config(wp_config=wp_config,
                     host=host,
                     port=port,
                     db_name=db_name,
                     user_credentials=user_credentials)

    database = Database(wp_config=wp_config)

    LOG.info('Checking if the specified database has already been set up...')
    if database.test_config():
        LOG.info('Successfully connected.')
        return

    LOG.info('Could not connect, so will set up the database.')
    database.ensure_database_setup(admin_credentials=admin_credentials)

    LOG.info('Validating the database setup...')
    if database.test_config(throw=True):
        LOG.info('Successfully connected.')
        return
