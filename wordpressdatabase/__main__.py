"""
"wordpressdatabase" entrypoint.
"""

import argparse
import logging

import wordpressdatabase

def run_from_cli():

    logging.basicConfig(level=logging.INFO)

    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument('--host',
                            help='database hostname',
                            required=True)

    arg_parser.add_argument('--admin-secret',
                            required=True)

    arg_parser.add_argument('--region',
                            required=False)

    args = arg_parser.parse_args()

    wordpressdatabase.ensure(
        host=args.host,
        engine='mysql',
        admin_credentials_secret_id=args.admin_secret,
        region=args.region)



if __name__ == '__main__':
    run_from_cli()
