from middleware.analysis import test_tfidf
import numpy as np
from middleware.analysis import svd

test_svd = svd.SVD()
u,s,v = test_svd.generate_truncated_svd(num_tweets=1000,num_topics=10)
reconstructed_vectors = u @ np.diag(s) @ v
vectors=test_svd.vectors
print(np.linalg.norm(reconstructed_vectors - vectors))
print(np.allclose(reconstructed_vectors, vectors))
print(np.allclose(u.T @ u, np.eye(u.shape[0])))
print(np.allclose(v @ v.T, np.eye(v.shape[0])))
print(test_svd.show_topics())