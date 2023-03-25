from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

docs = []
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(docs)


def compute_query_cosine_similarities(query):
    query_vector = vectorizer.transform([query])
    sims = cosine_similarity(query_vector, tfidf_matrix).flatten()
    return sims


def get_k_recommendations(query, k):
    sims = compute_query_cosine_similarities(query)
    indices = np.argsort(sims)[::-1][:k]
    return [docs[idx] for idx in indices]
