from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors

def train_model(data):
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(data['name'])
    model = NearestNeighbors(n_neighbors=1, algorithm='auto').fit(X)
    return vectorizer, model

def find_medicine(vectorizer, model, medicine_name):
    query_vec = vectorizer.transform([medicine_name])
    distances, indices = model.kneighbors(query_vec)
    return indices[0][0]
