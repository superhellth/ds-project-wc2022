from setuptools import setup

setup(name='middleware',
      version='1.0',
      packages=['middleware.data_collection',
                'middleware.data_retrieval',
                'middleware.tweet_management',
                'middleware.analysis'],
      install_requires=['tweepy', 'elasticsearch==7.17', 'fastapi[all]', 'pandas', 'gensim', 'matplotlib',
                        'scikit-learn', 'numpy', 'seaborn', 'tk', 'ujson', 'networkx', 'node2vec',
                        'vaderSentiment', 'transformers', 'torch==2.0.0', 'torchvision==0.15.1', 'gensim']

      )
