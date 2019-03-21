from setuptools import setup, find_packages
import sys, os

version = '0.0'

setup(name='karaRFSclient',
      version=version,
      description="a robot framework library based kara",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='of656',
      author_email='pangdinghai@ofpay.com',
      url='',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
