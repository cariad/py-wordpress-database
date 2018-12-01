"""
"wordpress-database" package setup.
"""

from setuptools import setup

setup(
    name='wordpressdatabase',
    version='0.1',
    description='Create and interact with a WordPress database.',
    url='https://github.com/cariad/py-wordpress-database',
    author='Cariad Eccleston',
    author_email='cariad@cariad.me',
    license='MIT',
    packages=[
        'wordpressdatabase'
    ],
    install_requires=[
        'boto3~=1.9.0',
        'mysql-connector~=2.1.0'
    ],
    extras_require={
        'dev': [
            'autopep8',
            'pylint'
        ]
    }
)
