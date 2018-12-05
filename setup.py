"""
wpdatabase package setup.
"""

from setuptools import setup

with open('README.md', 'r') as stream:
    LONG_DESCRIPTION = stream.read()

setup(
    author='Cariad Eccleston',
    author_email='cariad@cariad.me',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP :: Site Management'
    ],
    description='A Python package that sets up a WordPress database.',
    extras_require={
        'dev': [
            'autopep8',
            'coverage',
            'pylint'
        ]
    },
    install_requires=[
        'boto3~=1.9.0',
        'mysql-connector~=2.1.0',
        'wpconfigr~=1.0.0'
    ],
    name='wpdatabase',
    license='MIT',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    packages=[
        'wpdatabase',
        'wpdatabase.classes',
        'wpdatabase.exceptions'
    ],
    url='https://github.com/cariad/py-wordpress-database',
    version='1.0')
