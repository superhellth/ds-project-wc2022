from setuptools import setup

setup(name='middleware',
      version='1.0',
      packages=['middleware.data_collection',
                'middleware.data_retrieval',
                'middleware.tweet_management',
                'middleware.analysis'],
      install_requires=['tweepy', 'elasticsearch==7.17', 'fastapi[all]', 'pandas', 'spacy', 'gensim', 'matplotlib', 'scikit-learn', 'sklearn', 'numpy', 'seaborn', 'tk', 'ujson', 'networkx', 'node2vec']

      )