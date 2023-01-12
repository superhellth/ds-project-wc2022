from middleware.analysis import stat_provider

N = 3
stat_provider = stat_provider.StatProvider("./src/data/")
used_n_grams = []

def get_next_n_gram(current_string: str):
    """Return next moste likely n-gram."""
    current_words = current_string.split()
    if N > 1:
        current_last_words = " ".join(current_words[-(N-1):])
    else:
        current_last_words = ""
    next_n_gram = stat_provider.get_n_gram_that(n=N, starts_with=current_last_words, not_in=used_n_grams)
    used_n_grams.append(next_n_gram)
    return next_n_gram

def gen_tweet_from(string: str, length=18):
    string = string.lower().strip()
    for i in range(length):
        next_n_gram = get_next_n_gram(string)
        if next_n_gram is None:
            break
        string += " " + next_n_gram[N - 1]
        print(string)
    print(string)

print("Loading n-grams from file...")
stat_provider.load_n_grams(N)
print("Done!")

gen_tweet_from("Human rights")
gen_tweet_from("Messi can")
gen_tweet_from("I think")
