from setuptools import setup

setup(name='middleware',
      version='1.0',
      packages=['middleware.data_collection',
                'middleware.data_retrieval',
                'middleware.tweet_management',
                'middleware.analysis'],
      install_requires=['tweepy==4.13.0', 'elasticsearch==7.17', 'fastapi[all]==0.93.0', 'pandas==1.5.3', 'gensim==4.3.1', 'matplotlib==3.7.1',
                        'scikit-learn==1.2.2', 'numpy==1.24.2', 'seaborn==0.12.2', 'tk', 'ujson==5.7.0', 'networkx==2.8.8', 'node2vec==0.4.6',
                        'vaderSentiment==3.3.2', 'transformers==4.27.0', 'torch==1.13.1', 'torchvision==0.14.0', 'scipy==1.10.1',
                        'pytorch-lightning==1.7.7', 'aitextgen==0.6.0', 'torchmetrics==0.11.4']

      )
