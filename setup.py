# -*- coding: utf-8 -*-

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

config = {
    'description': '''kara is auto library packages for ofpay test team.\nMaybe... We're all just KARA''',
    'author': 'genvia',
    'url': 'http://www.vmovier.com/17863/',
    'download_url': '',
    'author_email': 'pangdinghai@ofpay.com',
    'version': '0.0.1',
    'packages': find_packages(),
    'install_requires': ['pytest', 'requests', 'SQLAlchemy', 'lxml',  'config', 'httmock', 'logbook', 'jsonpath-rw'],
    'scripts': ['bin/main.py'],
    'setup_requires': ['pytest-runner'],
    'tests_require': ['pytest'],
    'name': 'kara'
}

setup(**config)
if __name__ == "__main__":
    pass

# vim: set ft=python ai nu et ts=4 sw=4 tw=110:

