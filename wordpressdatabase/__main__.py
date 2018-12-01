"""
"wordpressdatabase" entrypoint.
"""

import argparse
import logging

import wordpressdatabase

from wordpressdatabase.classes import Credentials


def run_from_cli():

    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument('--log-level',
                            default='INFO',
                            help='log level')

    arg_parser.add_argument('--host',
                            help='database hostname',
                            required=True)

    arg_parser.add_argument('--port',
                            help='database port',
                            required=False)

    arg_parser.add_argument('--admin-credentials-secret-id',
                            required=True)

    arg_parser.add_argument('--db-name',
                            required=True)

    arg_parser.add_argument('--wp-username',
                            required=True)

    arg_parser.add_argument('--wp-password',
                            required=True)

    arg_parser.add_argument('--admin-username',
                            required=False)

    arg_parser.add_argument('--admin-password',
                            required=False)

    arg_parser.add_argument('--wp-config',
                            help='Path and filename of wp-config.php',
                            required=True)

    arg_parser.add_argument('--region',
                            required=False)

    args = arg_parser.parse_args()

    logging.basicConfig(level=str(args.log_level).upper())

    admin_credentials = Credentials(username=args.admin_username,
                                    password=args.admin_password,
                                    secret_id=args.admin_credentials_secret_id,
                                    region=args.region)

    user_credentials = Credentials(username=args.wp_username,
                                   password=args.wp_password)

    wordpressdatabase.ensure(wp_config_filename=args.wp_config,
                             admin_credentials=admin_credentials,
                             user_credentials=user_credentials,
                             host=args.host,
                             port=args.port,
                             db_name=args.db_name)

if __name__ == '__main__':
    run_from_cli()
