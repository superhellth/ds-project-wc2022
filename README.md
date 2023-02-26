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
- For the graph frontend (word graph and ne graph) we used code from the 'Explore' example from https://www.sigmajs.org/
- For the graph clustering we used code from this https://stackoverflow.com/questions/62902871/how-can-i-cluster-a-graph-g-created-in-networkx
- We used this as training and test data for our sentiment analysis https://www.kaggle.com/datasets/yasserh/twitter-tweets-sentiment-dataset
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
- In the root of the project type `docker compose up`
- Explore our
  - dashboard at `localhost:5173`
  - data-providing middleware at `localhost:8001/docs`
  - data-collection middleware at `localhost:8002/docs`
  - tweet-generation middleware at `localhost:8003/docs`

### Running frontend and middleware separately (only recommended for dev purposes)
#### Running the frontend
- Navigate to the `src/frontend` directory
- `npm install`
- `npm run dev`
#### Running the middleware
- Open the `main.py` in the `src/middleware/middleware/data_retrieval` directory and change the path to the data files to the absolute path to the `src/data` directory
*Only necessary if the default does not work*
- Navigate to the `src/middleware` directory
- `pip install [-e] .`
- Navigate to the `src/middleware/middleware/data_retrieval` directory
- `python[3] -m uvicorn main:app --reload`

*Note for Dennis: Many of our data files are too large for git. So without these files some functionalities are unavailable(the middleware just doesn't respond). These functionalities include: Dispaly of n-grams, Tweet generation based on n-grams, Custom collocation-graph building*

## Planning State
Our project currently features a fully functioning elasticsearch server that captured tweets about the FIFA World Cup in Qatar.
Additionally, we have a dashboard prototype. We agreed on a design and text analytics features we want to implement. The base functionality of the core features have been implemented. Some of them are not yet displayed on the frontend.

### Future planning
Moving forward, we plan to implement the following text analytics tasks as well as improve our dashboard to make it more visually appealing:
- Wordclouds: Common words, Entities
- Topic Modeling using NNMF/SVD to gain insights about topics discussed
- word embeddings
- basic stats about tweets and users (number of tweets/users, user with the most tweets/most followers, hashtags commonly used together...)
- sentiment analysis on the whole corpus to filter out sentiment by location, follower count etc.

### High-level Architecture Description
We split our project code into three parts. The **frontend** based on svelte, the **python middleware** for analysis tasks and as a connection to the **elasticsearch backend** that runs on our server.
All requests to elasticsearch are handled by the middleware. The frontend only loads data from local files or from the middleware but never directly accesses elasticsearch. But as stated above the middleware does not only provide a connection to the backend but is also where all analysis tasks take place. Here we write scripts to analyse and process our data.

### Already Done [27.01.2023]
- Data collection is done
- We wrote a script the allows us to annotate our collected tweets with custom labels. We already labeled 1000 Tweets
- Generated unigram, bigram, trigram and fourgram counts *(These files are not included in the repository since they are too large)*
- Generated collocation counts for a window size of 2, 3 and 4 *(These files are not included in the repository since they are too large)*
- Basic tweet completion tool based on n-grams
- Word graph based on collocation counts
- Sentiment analysis on a small user-defined set of tweets

### Experiments
We plan to implement a Tweet generator that uses more sophisticated machine learning methods.

## Current Code State
Our basic infrastructure is done. We can now comfortably access specific parts of our data an process it in parallel. The classes making up this infrastructure are well commented and (hopefully) understandably written. 

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
- Implement SVD and NMF for topic modeling.
