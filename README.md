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

## How to run our Dashboard
- Navigate to the `frontend` folder in Terminal, then
- `npm install`
- (These next 2 steps will be handled by a script later on. They are necessary because of a bug in the sveltestrap UI framework.)
  - Go to `src/frontend/node_module/@popperjs/`
  - Open `package.json` and append after line 4 ('description'): `  "type": "module",`
- `npm run dev`
- Enjoy :)


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

#Planned text analytic features
##Basic statistics
-Number of tweets posted over the course of time
-Share of tweets posted with the hashtags #lgtbq and #humanrights etc.
-OverView about tweets which are filtered out

##Textanalytic from the lecture
-Most common words displayed as wordcloud
-Topic modeling based on the collected tweets via NNMF or SVD
-Word respectively Entity Graph

##Textanalytics inspired by further research
-Modeling hashtags which appearing most common in combination


# Project Log
## November 2022

- Nico rented a server and set up elasticsearch and kibana on it.
- Nico continued with setting up a website based on svelte that was able to display the current rule we use to scrape Tweets as well as the latest 50 tweets that were harvested from Twitter.
- Raphael and Bastian focused on the first assignment during that timeframe.

## December 2022

- After our first meeting with our supervisor, we decided to each take on work for the upcoming assignments to contribute more equally to the project.
- We brainstormed ideas to implement such that each person will contribute something for the milestone.
- In the first two weeks of december we will implement some kind of text analytics tasks so that we will have a preview that we can show at our 'milestone' meeting mid December.
- Bastian changed the UI of the frontend from materials UI to sveltestrap. He also added the ability to create graphs/diagrams/etc. using the `chart.js` library.
