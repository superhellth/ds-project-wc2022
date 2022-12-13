from setuptools import setup

setup(name='middleware',
      version='1.0',
      packages=['middleware.data_collection',
                'middleware.data_retrieval',
                'middleware.tweet_management'],
      install_requires=['tweepy', 'elasticsearch', 'fastapi[all]']
      )