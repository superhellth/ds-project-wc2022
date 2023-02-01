import logging
import spacy
from gensim.models.phrases import Phrases, Phraser
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence

# setting up logging to monitor gensim
logging.basicConfig(format="%(levelname)s - %(asctime)s: %(message)s", datefmt= "%H:%M:%S", level=logging.INFO)

# nlp = spacy.load("en_core_web_sm", disable=["tagger", "parser", "ner", "lemmatizer"])
# stream = LineSentence("./src/data/tokenized_tweets_nostop_nohashtag.linesentence")
# phrases = Phrases(stream, min_count=100, threshold=30)
# with open("./src/data/tweet_phrases_nostop_nohashtag_mc=100_th=30.linesentence", "w") as f:
#     for tweet in stream:
#         f.write(" ".join(phrases[tweet]) + "\n")

# stream = LineSentence("./src/data/tweet_phrases_nostop_nohashtag_mc=100_th=30.linesentence")
# w2v = Word2Vec(min_count=2, vector_size=100, alpha=0.03, negative=20, window=3, min_alpha=0.0001, workers=4, sample=6e-5)
# w2v.build_vocab(stream)
# w2v.train(stream, epochs=25, total_examples=w2v.corpus_count)

# w2v.save("./src/data/w2v_epochs=25.emb")

model = Word2Vec.load("./src/data/w2v_epochs=25.emb")
print(model.wv.most_similar(positive=["cristiano_ronaldo", "messi"], negative=["ronaldo"]))
            

# with open("./src/data/tweet_phrases_nostop_nohashtag.linesentence", "r") as f:
#     text = str(f.read())
#     print("christiano_ronaldo" in text)
#     print("lionel_messi" in text)
#     print("human_rights" in text)
#     print("declan_rice" in text)

# tweet_list = []
# i = 0
# with open("./src/data/tokenized_tweets_nostop.txt", "r") as f:
#     as_text = f.read()
#     as_text = as_text[2:-2]
#     for tweet_str in as_text.split("],["):
#         a_tweet_list = []
#         i += 1
#         for token_str in tweet_str.split(","):
#             token_str = token_str.replace("\"", "")
#             if not token_str.startswith("#"):
#                 a_tweet_list.append(token_str)
#         tweet_list.append(a_tweet_list)
#         if i % 10000 == 0:
#             print(f"Loaded {i} Tweets from file...")

# with open("./src/data/tokenized_tweets_nostop_nohashtag.linesentence", "w") as f:
#     for tweet in tweet_list:
#         f.write(" ".join(tweet) + "\n")
