import logging
import spacy
from gensim.models.phrases import Phrases, Phraser
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence
from middleware.analysis import tweet_provider
from middleware.analysis import nlp_support

# setting up logging to monitor gensim
logging.basicConfig(format="%(levelname)s - %(asctime)s: %(message)s", datefmt= "%H:%M:%S", level=logging.INFO)

# stream = LineSentence("./src/data/tweet_phrases_nostop_nohashtag_mc=100_th=30.linesentence")
# w2v = Word2Vec(min_count=2, vector_size=100, alpha=0.03, negative=20, window=3, min_alpha=0.0001, workers=4, sample=6e-5)
# w2v.build_vocab(stream)
# w2v.train(stream, epochs=25, total_examples=w2v.corpus_count)

# w2v.save("./src/data/w2v_epochs=25.emb")

model = Word2Vec.load("./src/data/w2v_epochs=25.emb")
print(model.wv.most_similar(positive=["cristiano_ronaldo", "messi"], negative=["ronaldo"]))

# model = Word2Vec.load("./src/data/w2v.emb")
# print(model.wv.most_similar("ronaldo"))
