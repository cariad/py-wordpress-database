"""
wpdatabase CLI entrypoint.
"""

import argparse
import logging

import wpdatabase
from wpdatabase.classes import Credentials


def run_from_cli():
    """ Perform an update instigated from a CLI. """

    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument(
        '--admin-credentials-aws-secret-id',
        help='Amazon Web Services (AWS) Secrets Manager secret ID holding '
             'the admin credentials.',
        required=False)

    arg_parser.add_argument(
        '--admin-credentials-aws-region',
        help='Amazon Web Services (AWS) region in which the secret resides.',
        required=False)

    arg_parser.add_argument(
        '--admin-username',
        help='database admin user username',
        required=False)

    arg_parser.add_argument(
        '--admin-password',
        help='database admin user password',
        required=False)

    arg_parser.add_argument(
        '--wp-config',
        help='Path and filename of wp-config.php',
        required=True)

    arg_parser.add_argument(
        '--log-level',
        default='INFO',
        help='log level')

    args = arg_parser.parse_args()

    logging.basicConfig(level=str(args.log_level).upper())

    username = args.admin_username
    password = args.admin_password

    if (not username) != (not password):
        arg_parser.error(
            'You must specify both --admin-username and --admin-password or '
            'neither.')
        exit(1)

    secret_id = args.admin_credentials_aws_secret_id
    region = args.admin_credentials_aws_region

    if username and secret_id:
        arg_parser.error(
            'You cannot specify both --admin-username and '
            '--admin-credentials-aws-secret-id.')
        exit(2)

    if (not username) and (not secret_id):
        arg_parser.error(
            'You must specify either --admin-username or '
            '--admin-credentials-aws-secret-id.')
        exit(3)

    if username:
        credentials = Credentials.from_username_and_password(
            username=username,
            password=password)
    else:
        credentials = Credentials.from_aws_secrets_manager(
            secret_id=secret_id,
            region=region)

    wpdatabase.ensure(wp_config_filename=args.wp_config,
                      credentials=credentials)


if __name__ == '__main__':
    run_from_cli()
