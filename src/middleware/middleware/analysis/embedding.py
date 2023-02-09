from typing import Type
import sys
import logging
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence
from gensim.models.phrases import Phrases
import numpy as np
from sklearn.manifold import TSNE
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


class Embedder:
    """Created trained w2v model and takes care of the neccessary files.
    """

    def __init__(self, path_to_data_files, path_to_embed_files) -> None:
        self.path_to_data_files = path_to_data_files
        self.path_to_embed_files = path_to_embed_files
        logging.basicConfig(format="%(levelname)s - %(asctime)s: %(message)s",
                            datefmt="%H:%M:%S", level=logging.INFO)

    def create_tokenized_tweets_linesentence_file(self, min_count=100, threshold=30, limit=None):
        """Creates 2 file: One is the tokenized_tweets file converted to linesentence format. The other one takes the aformentioned file and converts
        the tokens into phrases(e. g. cristiano ronalod => cristiano_ronaldo)

        Args:
            min_count (int, optional): Minimal number of occurences of words to be taken into account for the final file. Defaults to 100.
            threshold (int, optional): Phrases threshold. Defaults to 30.
            limit (int or None, optional): Number of tweets to convert to linesentence format. If None all tweets are processed. Defaults to None.
        """
        tweet_list = []
        i = 0
        # read tokenized_tweets_nostop.txt and convert to linesentence format (one tweet per line, no "s)
        with open(self.path_to_data_files + "tokenized_tweets_nostop.txt", "r", encoding="utf_8") as f:
            as_text = f.read()
            as_text = as_text[2:-2]
            for tweet_str in as_text.split("],["):
                a_tweet_list = []
                i += 1
                for token_str in tweet_str.split(","):
                    token_str = token_str.replace("\"", "")
                    if not token_str.startswith("#"):
                        a_tweet_list.append(token_str)
                tweet_list.append(a_tweet_list)
                if i % 10000 == 0:
                    print(f"Loaded {i} Tweets from file...")

        # write into linesentence format without phrases
        with open(self.path_to_embed_files + "tokenized_tweets_nostop_nohashtag.linesentence", "w", encoding="utf_8") as f:
            for tweet in tweet_list:
                f.write(" ".join(tweet) + "\n")

        # write into linesentence with phrases
        stream = LineSentence(self.path_to_embed_files +
                              "tokenized_tweets_nostop_nohashtag.linesentence", limit=limit)
        phrases = Phrases(stream, min_count=min_count, threshold=threshold)
        file_name = "tweet_phrases_nostop_nohashtag_mc=" + \
            str(min_count) + "_th=" + str(threshold) + ".linesentence"
        with open(self.path_to_embed_files + file_name, "w", encoding="utf_8") as f:
            for tweet in stream:
                f.write(" ".join(phrases[tweet]) + "\n")

    def create_w2vec_model(self, min_count=2, vector_size=100, alpha=0.03, negative=20, window=3, min_alpha=0.0001, workers=4, sample=6e-5, epochs=100):
        """Create and train Word2Vec model with the given parameters.

        Args:
            min_count (int, optional): Passed to Word2Vec. Defaults to 2.
            vector_size (int, optional): Passed to Word2Vec. Defaults to 100.
            alpha (float, optional): Passed to Word2Vec. Defaults to 0.03.
            negative (int, optional): Passed to Word2Vec. Defaults to 20.
            window (int, optional): Passed to Word2Vec. Defaults to 3.
            min_alpha (float, optional): Passed to Word2Vec. Defaults to 0.0001.
            workers (int, optional): Passed to Word2Vec. Defaults to 4.
            sample (_type_, optional): Passed to Word2Vec. Defaults to 6e-5.
            epochs (int, optional): Number of epochs to train the model on. Defaults to 100.

        Returns:
            Word2Vec: Trained model.
        """
        stream = LineSentence(
            "./src/data/tweet_phrases_nostop_nohashtag_mc=100_th=30.linesentence")
        w2v = Word2Vec(min_count=min_count, vector_size=vector_size, alpha=alpha,
                       negative=negative, window=window, min_alpha=min_alpha, workers=workers, sample=sample)
        w2v.build_vocab(stream)
        w2v.train(stream, epochs=epochs, total_examples=w2v.corpus_count)
        return w2v

    def tsneplot(self, model: Type[Word2Vec], word: str, num_closest: int = 10, num_furthest: int = 0):
        """Create TSNE plot for a word in a Word2Vec model.

        Args:
            model (Type[Word2Vec]): Word2Vec model.
            word (str): Word to create graph for.
        """
        embs = np.empty((0, 100), dtype="f")
        word_labels = [word]
        color_list = ["green"]

        embs = np.append(embs, [model.wv[word]], axis=0)


        close_words = model.wv.most_similar(word, topn=num_closest)
        # adds the vector for each of the closest words to the array
        for wrd_score in close_words:
            wrd_vector = model.wv[wrd_score[0]]
            word_labels.append(wrd_score[0])
            color_list.append("blue")
            embs = np.append(embs, [wrd_vector], axis=0)

        if num_furthest != 0:
            all_sims = model.wv.most_similar(word, topn=sys.maxsize)
            far_words = list(reversed(all_sims[-num_furthest:]))
            # adds the vector for each of the furthest words to the array
            for wrd_score in far_words:
                wrd_vector = model.wv[wrd_score[0]]
                word_labels.append(wrd_score[0])
                color_list.append("red")
                embs = np.append(embs, [wrd_vector], axis=0)

        np.set_printoptions(suppress=True)
        Y = TSNE(n_components=2, learning_rate=200, random_state=42,
                 perplexity=num_closest + num_furthest - 5, init="random").fit_transform(embs)

        # sets everything up to plot
        df = pd.DataFrame({"x": [x for x in Y[:, 0]],
                           "y": [y for y in Y[:, 1]],
                           "words": word_labels,
                           "color": color_list})

        fig, _ = plt.subplots()
        fig.set_size_inches(10, 10)

        # basic plot
        p1 = sns.regplot(data=df,
                         x="x",
                         y="y",
                         fit_reg=False,
                         marker="o",
                         scatter_kws={"s": 40, "facecolors": df["color"]}
                         )

        # adds annotations one by one with a loop
        for line in range(0, df.shape[0]):
            p1.text(df["x"][line],
                    df["y"][line],
                    "  " + df["words"][line].title(),
                    horizontalalignment="left",
                    verticalalignment="bottom", size="medium",
                    color=df["color"][line],
                    weight="normal"
                    ).set_size(15)

        plt.xlim(Y[:, 0].min()-50, Y[:, 0].max()+50)
        plt.ylim(Y[:, 1].min()-50, Y[:, 1].max()+50)

        plt.title("t-SNE visualization for {}".format(word.title()))
