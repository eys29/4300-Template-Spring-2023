from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD
import numpy as np

def edit_distance(query, message):
    query = query.lower()
    message = message.lower()
    m = len(query) + 1
    n = len(message) + 1
    delete = 1
    insert = 1
    substitute = 2

    edit_matrix = np.zeros((m, n))
    for i in range(1, m):
        edit_matrix[i][0] = edit_matrix[i-1][0] + delete
    for j in range(1, n):
        edit_matrix[0][j] = edit_matrix[0][j-1] + insert
    for i in range(1, m):
        for j in range(1, n):
            edit_matrix[i][j] = min(
                edit_matrix[i-1][j] + delete,
                edit_matrix[i][j-1] + insert,
                edit_matrix[i-1][j-1] +
                (0 if query[i-1] == message[j-1] else substitute)
            )
    return edit_matrix[m-1][n-1]


def get_menu_items_recommendations(query, menu_items, limit=10, sim_threshold=0.35):
    if len(menu_items) == 0: return []
    vectorizer = TfidfVectorizer()
    menu_items_str = [item[0].str_rep() for item in menu_items]
    tfidf = vectorizer.fit_transform(menu_items_str)
    svd = TruncatedSVD(n_components=40)
    svd_docs = svd.fit_transform(tfidf)
    query_tfidf = vectorizer.transform([query])
    query_vec = svd.transform(query_tfidf)
    sims = cosine_similarity(query_vec, svd_docs).flatten()
    indices = np.argsort(sims)[::-1]
    if len(indices) > limit:
        indices = indices[:limit]
    indices = [idx for idx in indices if sims[idx] >= sim_threshold]
    items_sorted_by_sim = [menu_items[idx] for idx in indices]
    items_sorted_by_rating = sorted(items_sorted_by_sim, key=lambda x: x[1], reverse=True)
    return [item[0] for item in items_sorted_by_rating]