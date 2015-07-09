import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

requires = [
    'requests>=2.2.1',
    'tweepy',
    'requests_oauthlib',
    'oauthlib',
    ]

setup(name='TwitterSearchLogger',
      version='0.0.1',
      description='log Twitter search result',
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP",
        ],
      author='',
      author_email='',
      url='',
      keywords='web twitter',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite="",
      entry_points="""\
      [paste.app_factory]
      main = TwitterSearchLogger:main
      """,
      )
