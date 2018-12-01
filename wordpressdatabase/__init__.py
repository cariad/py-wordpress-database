"""
"wordpressdatabase" package initialization.
"""

import json
import logging

import boto3

from mysql.connector import connect

from wordpressdatabase.classes import Credentials
from wordpressdatabase.exceptions import UnhandledEngineError


def is_valid_database_name(name):
    for c in name:
        if not str.isalnum(c) or c != '_':
            return False
    return True


def ensure(engine,
           host,
           wp_username,
           wp_password,
           admin_username=None,
           admin_password=None,
           admin_credentials_secret_id=None,
           db_name='wordpress',
           port=None,
           region=None):

    if engine != 'mysql':
        raise UnhandledEngineError()

    admin_credentials = Credentials(username=admin_username,
                                    password=admin_password,
                                    secret_id=admin_credentials_secret_id,
                                    region=region)

    if not is_valid_database_name(db_name):
        raise Exception('Invalid database name.')

    logger = logging.getLogger(__name__)

    logger.info('Connecting to %s...', host)

    conn = connect(
        host=host,
        port=port,
        user=admin_credentials.username,
        passwd=admin_credentials.password)

    cursor = conn.cursor()

    logger.info('Ensuring database "%s" exists...', db_name)

    # Database names cannot be parameterized, so validate it and be careful.
    cursor.execute('CREATE DATABASE IF NOT EXISTS {};'.format(db_name))

    logger.info('Ensuring user "%s" exists...', wp_username)
    cursor.execute('GRANT ALL PRIVILEGES ON {} TO %s IDENTIFIED BY %s;'.format(db_name),
                   (wp_username, wp_password))

    logger.info('Flushing privileges...')
    cursor.execute('FLUSH PRIVILEGES;')

    logger.info('Committing transaction...')
    conn.commit()

    logger.info('Closing connection...')
    cursor.close()
    conn.close()

    logger.info('Done.')
