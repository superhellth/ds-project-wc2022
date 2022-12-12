# 'Sportswashing' - Can Qatar improve its reputation by hosting the FIFA World Cup?

## Team Members

- Raphael Ebner, 4170420, B.Sc. Informatik
- Nicolas Hellthaler, 4164933, B.Sc. Informatik
- Bastian Müller, 4138763, B.Sc. Angewandte Informatik
- chatGPT by OpenAI

## Mail Addresses

- raphael.ebner@stud.uni-heidelberg.de
- nicolas.hellthaler@stud.uni-heidelberg.de
- bastian.mueller@stud.uni-heidelberg.de
- Reachable at https://chat.openai.com/chat

## Existing Code Fragments

- For our dashboard we made use of this template (https://github.com/GeekyAnts/sb-admin-svelte)
  - We rewrote most of the code but copied some pieces that we liked a lot about the template
- We also use Bootstrap CSS for styling and Icons

## Utilized Libraries

*Note: requirements.txt is not setup yet.*
- List of required python libraries to run our system (middleware), so far:
  - fastapi
  - tweepy
  - elasticsearch

- List of required node.js/svelte libraries to run our system (frontend), so far:
  - see `package.json` in `frontend` folder for dependencies

## Contributions
*In case some team members contributed to the project in a way that is not clear from the commit history, you can mention their contributions here.*

chatGPT helped us a lot so far, therefore we welcome the AI as an unofficial member of our Team.

## Uploading for Other Team Members

*If you are pushing code for another team member, you should indicate their name in the commit message.*

Noting yet.


# Project state

## Our data
- Our twitter-api query string looks like this: `#Qatar2022 OR #QatarWorldCup2022 OR  #fifaworldcup2022 OR #Roadto2022 OR @FIFAWorldCup OR @roadto2022en OR (#qatar #lgbtq) OR (#qatar #humanrights) OR context:29.1275806388367720450 OR context:6.1275806388367720450) -is:retweet -is:reply -is:quote lang:en`
- During the K.O. stage of the World Cup there are some time periods for which we don't have any data since even 3 elevated twitter-api accounts are not enough to capture every tweet.
- (12.12.2022) Our data consists of about 4.5 million tweets

## How to run our Dashboard
- Navigate to the `frontend` folder in Terminal, then
- `npm install`
- (These next step will be handled by a script later on. It is necessary because of a bug in the `sveltestrap` UI framework.)
  - Go to `src/frontend/node_module/@popperjs/`
  - Open `package.json` and append after line 4 ('description'): `  "type": "module",`
- `npm run dev`
- Enjoy :)

## Planning State
Our project currently features a fully functioning elasticsearch server that captures tweets about the ongoing FIFA World Cup in Qatar.
Additionally, we have a dashboard prototype. We agreed on a design and text analytics features we want to implement.
We will start working on the text analytics tasks in the second half of December since we now have then necessary understanding from the lectures as well as some data to use it on.
We are currently working on a template for all (interactive) charts. (Likely not ready yet)

### Future planning
Moving forward, we plan to implement text analytics tasks of our data as well as improve our dashboard to make it more visually appealing.
Below are some features we want to implement specifically.

### High-level Architecture Description
We split our project code into two parts. `frontend` for the dashboard based on svelte and `middleware` for connection to elasticsearch that runs on our server as backend.
Like we said in our proposal, we saved several attributes of tweets, that are connected (by a specific hashtag or topic or linked user) to the World Cup.
We also saved aspects certain attributes of the user such as the age of the account, the username and the name.

The analysis will be done in the middleware as well. We plan to have some interactive graphs that will be generated on the users machine and getting data directly from our server.
Other graphs will be based on an analysis/data that comes with the projects code because generating it would take too much time.
We'll use json files for storing our data.

### Experiments
Since we focused on building a dashboard we can work with and an elasticsearch pipeline, we did not experiment with our data yet.
We'll start to explore it more over the coming weeks, when we build our text analytics tasks.

### Basic statistics

- Number of tweets posted over the course of time
- Share of tweets posted with the hashtags #lgtbq and #humanrights etc.
- OverView about tweets which are filtered out

### Text analytics from lecture

- Most common words displayed as wordcloud
- Topic modeling based on the collected tweets via NNMF or SVD
- Word respectively Entity Graph

### Text analytics inspired by further research

- Modeling hashtags that appear often in combination with each other

### Examples
Please start our dashboard and click on 'Graph 1' to see the 50 most current tweets that our elasticsearch server captured.

## Current Code State
The code is not documented perfectly yet. We will improve our documentation over the coming weeks.
We plan to use docstrings.

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
