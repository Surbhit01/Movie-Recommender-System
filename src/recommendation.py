from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd
import re

class recommendation:
    
    def load_and_clean_data(self):
        self.movies = pd.read_csv('../data/movies.csv')
        self.rating = pd.read_csv('../data/ratings.csv')
        self.vectorizer = TfidfVectorizer(ngram_range=(1,2))
        self.movies["clean_title"] = self.movies["title"].apply(clean_title)
        self.tfidf = self.vectorizer.fit_transform(self.movies['clean_title'])
        
        #print('Dateset loaded and cleaned')

    def search_title(self,title):
        title = clean_title(title)
        query_vec = self.vectorizer.transform([title])
        similarity = cosine_similarity(query_vec, self.tfidf).flatten()
        indices = np.argpartition(similarity, -5)[-5:]
        results = self.movies.iloc[indices][::-1]
        return results.iloc[0]["movieId"]
    
    def find_similar_movies(self,movie_id):
        similar_users = self.rating[(self.rating["movieId"] == movie_id) &  (self.rating["rating"] > 4)]["userId"].unique()
        similar_users_recs = self.rating[(self.rating["userId"].isin(similar_users)) & (self.rating["rating"] > 4)]["movieId"]
        
        similar_users_recs = similar_users_recs.value_counts() / len(similar_users)
        similar_users_recs = similar_users_recs[similar_users_recs > 0.1]
        
        all_users = self.rating[(self.rating["movieId"].isin(similar_users_recs.index)) & (self.rating['rating']>4)]
        all_users_recs = all_users['movieId'].value_counts() / len(all_users['userId'].unique())
        
        rec_percentage = pd.concat([similar_users_recs, all_users_recs], axis=1)
        rec_percentage.columns = ['Similar Users', 'All Users']
        
        rec_percentage['Score'] = rec_percentage['Similar Users'] / rec_percentage['All Users']
        
        rec_percentage = rec_percentage.sort_values("Score", ascending=False)
        
        return rec_percentage.head(10).merge(self.movies, left_index=True, right_on="movieId")[["Score","title","genres"]]

def clean_title(title):
        return re.sub("[^a-zA-Z0-9 ]","",title)    





