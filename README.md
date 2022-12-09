# 'Sportswashing' - Can Qatar improve its reputation by hosting the FIFA World Cup?

## Team Members

- Raphael Ebner, 4170420, B.Sc. Informatik
- Nicolas Hellthaler, 4164933, B.Sc. Informatik
- Bastian Müller, 4138763, B.Sc. Angewandte Informatik

## Mail Addresses

- ve257@stud.uni-heidelberg.de
- nicolas.hellthaler@stud.uni-heidelberg.de
- bastian.mueller@stud.uni-heidelberg.de

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
  - Except for the SideBar, we did not "copy and paste" anything, but wrote our own implementation
- We also use Bootstrap CSS and Icons

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

Nothing yet.

## Uploading for Other Team Members

*If you are pushing code for another team member, you should indicate their name in the commit message.*

Noting yet.



# Project Log
## November 2022

- Nico rented a server and set up elasticsearch and kibana on it.
- Nico continued with setting up a website based on svelte that was able to display the current rule we use to scrape Tweets as well as the latest 50 tweets that were harvested from Twitter.
- Raphael and Bastian focused on the first assignment during that timeframe.

## December 2022

- After our first meeting with our supervisor, we decided to each take on work for the upcoming assignments to contribute more equally to the project.
- We brainstormed ideas to implement such that each person will contribute something for the milestone.
- In the first two weeks of december we will each implement some kind of text analytics task so that we will have some kind of preview that we can show at our 'milestone' meeting mid December.
