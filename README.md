# py-wordpress-database

[![CircleCI](https://circleci.com/gh/cariad/py-wordpress-database/tree/master.svg?style=svg)](https://circleci.com/gh/cariad/py-wordpress-database/tree/master)

A Python package that sets up a WordPress database.

`wpdatabase` will:
 - Create the database, if it doesn't exist already.
 - Create the WordPress user, if it doesn't exist already.

`wpdatabase` is idempotent; if the database and the user already exist then it will return successfully.

Note that `wpdatabase` currently only supports MySQL databases.

## Installation

```shell
pip install wpdatabase
```

## Prerequisites

`wpdatabase` assumes that the following properties have already been set in the `wp-config.php` file:

| Property      | Description
|-              |-
| `DB_HOST`     | Host or endpoint of the MySQL database server.
| `DB_USER`     | WordPress database user.
| `DB_PASSWORD` | WordPress database password.

If you need help adding these values to `wp-config.php` then check out [wpconfigr](https://github.com/cariad/py-wpconfigr).

## Command-line usage

If you need to specify to the database's administrator username and password:

```shell
python -m wpdatabase --wp-config      /www/wp-config.php \
                     --admin-username garnet \
                     --admin-password love
```

If you're deploying WordPress into Amazon Web Services (AWS) and have your administrator username and password held in Secrets Manager:

```shell
python -m wpdatabase --wp-config                       /www/wp-config.php \
                     --admin-credentials-aws-secret-id AdminSecretID \
                     --admin-credentials-aws-region    eu-west-1
```

## Development

To install development dependencies:

```shell
pip install -e .[dev]
```

To run the tests:

```shell
python test.py
```

## Changes

### v1.0.1 - 2018-12-11

Fixed broken dependency versions.

### v1.0 - 2018-12-05

Initial release.
