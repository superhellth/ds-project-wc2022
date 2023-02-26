# 'Sportswashing' - Can Qatar improve its reputation by hosting the FIFA World Cup?

## Team Members

- Raphael Ebner, 4170420, B.Sc. Informatik
- Nicolas Hellthaler, 4164933, B.Sc. Informatik
- Bastian Müller, 4138763, B.Sc. Angewandte Informatik
- (chatGPT by OpenAI)

## Mail Addresses

- raphael.ebner@stud.uni-heidelberg.de
- nicolas.hellthaler@stud.uni-heidelberg.de
- bastian.mueller@stud.uni-heidelberg.de
- (At least sometimes) reachable at https://chat.openai.com/chat

## Existing Code Fragments

- For our dashboard we made use of this template (https://github.com/GeekyAnts/sb-admin-svelte)
  - We rewrote most of the code but copied some pieces that we liked a lot about the template
- For the graph frontend (word graph and ne graph) we used code from the 'Explore' example from (https://www.sigmajs.org/)
- For the graph clustering we used code from this (https://stackoverflow.com/questions/62902871/how-can-i-cluster-a-graph-g-created-in-networkx)
- We used this as training and test data for our sentiment analysis (https://www.kaggle.com/datasets/yasserh/twitter-tweets-sentiment-dataset)
- The TSNE plots on the embedding page are generated using Code from the IDSTA lecture 2022/23 at Heidelberg University, Assignment 3

## Utilized Libraries

- List of required python libraries to run our middleware can be found in the `src/middleware/setup.py` file
- List of required js libraries to run our frontend can be found in the `src/frontend/package.json` file

# Project state

## Our data
- Our twitter-api query string looks like this: `#Qatar2022 OR #QatarWorldCup2022 OR  #fifaworldcup2022 OR #Roadto2022 OR @FIFAWorldCup OR @roadto2022en OR (#qatar #lgbtq) OR (#qatar #humanrights) OR context:29.1275806388367720450 OR context:6.1275806388367720450) -is:retweet -is:reply -is:quote lang:en`
- During the K.O. stage of the World Cup there are some time periods for which we don't have any data since even 3 elevated twitter-api accounts are not enough to capture every tweet.
- Our data consists of 5,025,511 tweets

## How to run our Dashboard
### Running frontend and middleware via Docker
*Note: Our project is quite large*
- In the root directory create a file called `.env`
- In this file paste and complete:
```
PUBLIC_DATA_RETRIEVAL_MIDDLEWARE_PORT=8001
PUBLIC_DATA_COLLECTION_MIDDLEWARE_PORT=8002
PUBLIC_TWEET_GENERATION_MIDDLEWARE_PORT=8003
SSH_HOST=[SSH Host of the server providing the data files that are too large for git. Format: username@IP]
SSH_PASSWD=[SSH Password of the above mentioned server]
PATH_TO_DATA_FILES=../../../data/
ES_URL=http://[IP of the server running Elasticsearch]:9200
ES_INDEX=tweets
ES_USERNAME=[Username of the Elasticsearch instance used]
ES_PASSWD=[Password of the Elasticsearch instance used]
BEARER_TOKEN=[Bearer Token for the Twitter API]
```
- In the root of the project type `docker compose up`
- Explore our
  - dashboard at `localhost:5173`
  - data-providing middleware at `localhost:8001/docs`
  - data-collection middleware at `localhost:8002/docs`
  - tweet-generation middleware at `localhost:8003/docs`

## Planning State
Our project currently features a fully functioning Elasticsearch server that captured tweets about the FIFA World Cup in Qatar. The Dashboard is fully implemented and the project has full Docker support.

### Future planning
If we had more time we would tackle the following points:
- Improve UI

### High-level Architecture Description
We split our project code into three parts. The **frontend** based on svelte, the **python middleware** for analysis tasks and as a connection to the **elasticsearch backend** that runs on our server.
All requests to elasticsearch are handled by the middleware. The frontend only loads data from local files or from the middleware but never directly accesses elasticsearch. But as stated above the middleware does not only provide a connection to the backend but is also where all analysis tasks take place. Here we write scripts to analyse and process our data.

### Already Done [26.02.2023]
- Data collection is done
- We wrote a script the allows us to annotate our collected tweets with custom labels. We already labeled 1000 Tweets
- Generated unigram, bigram, trigram and fourgram counts *(These files are not included in the repository since they are too large)*
- Generated collocation counts for a window size of 2, 3 and 4 *(These files are not included in the repository since they are too large)*
- Word graph based on collocation counts
- Sentiment analysis on the whole corpus
- SVD and NMF on >1,000,000 Tweets
- Word embeddings using Word2Vec
- Basic tweet completion tool based on n-grams
- Tweet Generation using GPT-Neo

## Current Code State
Our functionality is done. Our classes are mostly well commented and (hopefully) understandably written. The frontend code still requires some refactoring.

# Project Log
## November 2022
- Nico rented a server and set up elasticsearch and kibana on it.
- Nico continued with setting up a website based on svelte that was able to display the current rule we use to scrape Tweets as well as the latest 50 tweets that were harvested from Twitter.
- Raphael and Bastian focused on the first assignment during that timeframe.

## December 2022
- After our first meeting with our supervisor, we decided to each take on work for the upcoming assignments to contribute more equally to the project.
- We brainstormed ideas to implement such that each person will contribute equally to the project.
- Bastian changed the UI of the frontend from `materials UI` to `sveltestrap`. He also added the ability to create graphs/diagrams/etc. using the `chart.js` library.
- We now have a Docker infrastructure set up for the middleware. We still have to figure out a workflow for Docker though.
- Improved our access to our data by writing a python class that provides the data in various data formats and allows filtering as well as sorting.
- Started labeling our own data to hopefully have high quality training data for classification tasks.
- Generated n-gram and collocation counts.

## January 2023
- Implement a word graph based on the collocation counts. Include clustering using different algorithms.
- Implement sentiment analysis with different methods and apply it to a small number of tweets.
- Add basic statistics about our tweets(e. g. age of accounts that posted tweets, their locations...)

## February 2023
- Add an entity-collocation graph.
- Implement Word Embeddings for our corpus. We now have a Word2Vec model trained on the whole corpus.
- Implement SVD and NMF for topic modeling.
- Extend Sentiment Analysis. Analysis was applied to the whole corpus split into topics.
- Major UI Improvements.
