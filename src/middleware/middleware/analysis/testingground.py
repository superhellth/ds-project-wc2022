from middleware.analysis import test_tfidf
import numpy as np
tfidf = test_tfidf.Test_TF_IDF()
matrix = tfidf.calculate_cosine_similarity()
print(matrix)
print(len(matrix))
print(len(matrix[0]))
"""for i in range(5):
    print(tfidf.corpus[i])
    print("_______________")
    print(tfidf.corpus[5])
    print("_______________")
    print(matrix[i][5])"""

def find_highest_n_indices(matrix, n):
    # Flatten the matrix
    flattened_matrix = matrix.flatten()
    # Find the shape of the matrix
    rows, cols = matrix.shape
    # Create a boolean mask to exclude elements on the main diagonal
    mask = np.arange(rows * cols) % (cols + 1) != 0
    # Exclude elements on the main diagonal
    flattened_matrix = flattened_matrix[mask]
    indices = np.arange(rows * cols)[mask]
    # Sort the remaining elements in descending order
    sorted_indices = np.argsort(flattened_matrix)[::-1][:n]
    result = indices[sorted_indices]
    
    return cols,result
n=5

cols,indices = find_highest_n_indices(matrix, n)
for i in indices:
    row = i // cols
    col = i % cols
    print("______________________________")
    print(row,col)
    print("###########")
    print("Element at ({}, {}) is {}".format(tfidf.corpus[row], tfidf.corpus[col], matrix[row][col]))