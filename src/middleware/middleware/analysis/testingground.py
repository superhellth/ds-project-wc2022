from middleware.analysis import test_tfidf
import numpy as np
tfidf = test_tfidf.Test_TF_IDF()
matrix = tfidf.calculate_cosine_similarity()

k=[]
for i in range(len(matrix)):
    for j in range(i+1,len(matrix[0])):
        if matrix[i][j] >=1 and i!=j:
            if tfidf.corpus[i]!=tfidf.corpus[j]:
                k.append([tfidf.corpus[i],tfidf.corpus[j],matrix[i][j]])
for i in range(len(k)):
    print("____________________")
    print(k[i])
    print("____________________")
print(len(k))
#x = tfidf.n_highest_tfidf()