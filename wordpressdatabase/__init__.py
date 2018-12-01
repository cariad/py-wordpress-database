"""
"wordpressdatabase" package initialization.
"""

import json
import logging

import boto3

from mysql.connector import connect

from wordpressdatabase.exceptions import InvalidParametersError
from wordpressdatabase.exceptions import UnhandledEngineError


def ensure(engine,
           host,
           admin_username=None,
           admin_password=None,
           admin_credentials_secret_id=None,
           db_name='wordpress',
           port=None):

    if engine != 'mysql':
        raise UnhandledEngineError()

    if admin_username and not admin_password:
        raise InvalidParametersError(
            'Must specify the admin password if you specify the admin username.')

    if not admin_username and admin_password:
        raise InvalidParametersError(
            'Must specify the admin username if you specify the admin password.')

    if (admin_username and admin_credentials_secret_id) or (not admin_username and not admin_credentials_secret_id):
        raise InvalidParametersError(
            'Must specify the admin credentials explicitly or via a secret.')

    if admin_credentials_secret_id:
        admin_username, admin_password = _get_credentials(
            admin_credentials_secret_id)

    conn = connect(
        host=host,
        user=admin_username,
        passwd=admin_password)

    cursor = conn.cursor()
    response = cursor.execute('CREATE DATABASE IF NOT EXISTS %s;', (db_name))

    cursor.close()
    conn.close()

    print(str(response))


def _get_credentials(secret_id,
                     username_key='username',
                     password_key='password'):

    client = boto3.client('secretsmanager')
    response = client.get_secret_value(SecretId=secret_id)
    secret_string = response['SecretString']
    secret = json.loads(secret_string)
    return secret[username_key], secret[password_key]
