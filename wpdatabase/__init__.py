"""
A Python package for creating and interacting with WordPress databases.
"""

import json
import logging

import boto3

from mysql import connector
from wpconfigr import WpConfigFile

from wpdatabase.classes import Database


def ensure(wp_config_filename, credentials):
    """
    Ensures that a WordPress database is set up according to the configuration
    in "wp-config.php".

    Args:
        wp_config_filename (str):  Path and filename of "wp-config.php".
        credentials (Credentials): Database admin user credentials.

    Raises:
        InvalidDatabaseNameError: The database name is invalid.
    """

    log = logging.getLogger(__name__)

    wp_config = WpConfigFile(filename=wp_config_filename)
    database = Database(wp_config=wp_config)

    log.info('Checking if the specified database has already been set up...')
    if database.test_config():
        log.info('Successfully connected.')
        return

    log.info('Could not connect, so will set up the database.')
    database.ensure_database_setup(credentials=credentials)

    log.info('Validating the database setup...')
    if database.test_config(throw=True):
        log.info('Successfully connected.')
