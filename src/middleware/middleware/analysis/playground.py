from middleware.analysis import nlp_support

n_gram_generator = nlp_support.Tokenizer()

n_gram_generator.generate_n_grams(2, "")
