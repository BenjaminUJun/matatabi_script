import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.txt')) as f:
    README = f.read()

requires = [
    'requests',
    'tweepy',
    'requests_oauthlib',
    ]

setup(name='TwitterSearchLogger',
      version='0.0.1',
      description='log Twitter search result',
      long_description=README,
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
