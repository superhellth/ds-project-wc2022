import os
import sys
from dotenv import load_dotenv
from aitextgen import aitextgen
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from middleware.analysis import stat_provider
from middleware.analysis import tweet_gen

### loading env variables ###
print("Trying to read preset environment variables...")
if os.getenv("PATH_TO_DATA_FILES") is None:
    print("Error.")
    print("Trying to load local dotenv file...")
    print()
    load_dotenv()

try:
    PATH_TO_DATA_FILES = os.getenv("PATH_TO_DATA_FILES")
except:
    print("Error.")
    print(
        "You have to provide the following environment variables: PATH_TO_DATA_FILES either as dotenv file or by setting the manually.")
    sys.exit()

print("Successfully read environment variables!")
print(f"Reading data from: {PATH_TO_DATA_FILES}")

## path to data files
# Bastian: /Users/bastianmuller/Desktop/Studium/Informatik_HD/7_HWS22:23/INF_ITA/Project/code/src/data/
# Nico: ../../../data/
PATH_TO_GENERATOR_MODEL = PATH_TO_DATA_FILES + "generator-model/"

print("Preparing n-gram data...")
stat_provider = stat_provider.StatProvider(path_to_data_files=PATH_TO_DATA_FILES)
tweet_generator = tweet_gen.TweetGenerator(provider=stat_provider)

## fastapi config
app = FastAPI()
origins = [
    "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

## generate tweets
prompt_ai = aitextgen(model_folder=PATH_TO_GENERATOR_MODEL)


## generate tweet with fine tuned gpt-neo model
@app.get("/analysis/finetunedgptneo/generate")
async def get_n_gen_tweets(prompt=None, temperature=0.7, repetition_penalty=1.2, length_penalty=1.2, n=1):
    res = []
    for _ in range(int(n)):
        res.append(prompt_ai.generate_one(prompt=prompt,
                                          temperature=float(temperature),
                                          repetition_penalty=float(repetition_penalty),
                                          length_penalty=float(length_penalty))[:-1])
    return res

# ## generate tweet based on n-grams
@app.get("/analysis/ngrams/generate")
async def generate_tweet_from_n_grams(given, tweet_length, n, percent_n_grams, allow_repitition):
    tweet_length = int(tweet_length)
    n = int(n)
    percent_n_grams = float(percent_n_grams)
    allow_repitition = allow_repitition == "True"
    return tweet_generator.gen_tweet_from(given, tweet_length, n, percent_n_grams, allow_repitition)
