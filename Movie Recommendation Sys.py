# -*- coding: utf-8 -*-
"""
Created on Sun Mar 26 16:04:38 2023

@author: Keerthana
"""

import pandas as pd
import numpy as np


movies=pd.read_csv("TMDB/tmdb_5000_movies.csv")
credits=pd.read_csv("TMDB/tmdb_5000_credits.csv")

movies=movies.merge(credits,on='title')

movies=movies[['movie_id','title','overview','genres','keywords','cast','crew',]]
movies=movies.dropna()

import ast
ast.literal_eval('[{"id": 28, "name": "Action"}, {"id": 12, "name": "Adventure"}, {"id": 14, "name": "Fantasy"}, {"id": 878, "name": "Science Fiction"}]')

def genresconvert(obj):
    l=[]
    for i in ast.literal_eval(obj):
        l.append(i['name'])
    return l       
movies['genres']=movies['genres'].apply(genresconvert)
movies['keywords']=movies['keywords'].apply(genresconvert)

def castconvert(obj):
    l=[]
    counter=0
    for i in ast.literal_eval(obj):
        if counter<4:
            l.append(i['name'])
        counter =counter+1
    return l

movies['cast']=movies['cast'].apply(castconvert)

def crewconvert(obj):
    l=[]
    counter=0
    for i in ast.literal_eval(obj):
        if i['job']=='Director':
            l.append(i['name'])
    return l


movies['crew']=movies['crew'].apply(crewconvert)


def collapse(obj):
    l=[]
    for i in obj:
        l.append(i.replace(" ",""))
    return l

movies['cast']=movies['cast'].apply(collapse)
movies['genres']=movies['genres'].apply(collapse)
movies['keywords']=movies['keywords'].apply(collapse)
movies['crew']=movies['crew'].apply(collapse)


movies['overview']=movies['overview'].apply(lambda x:x.split())

movies['tags']=movies['overview']+movies['genres']+movies['keywords']+movies['cast']+movies['crew']
new = movies.drop(columns=['overview','genres','keywords','cast','crew'])
new['tags']=new['tags'].apply(lambda x: " ".join(x))
new['tags']=new['tags'].apply(lambda x:x.lower())


import nltk
from nltk.stem.porter import PorterStemmer
ps= PorterStemmer()
def stem(text):
    y=[]
    for i in text.split():
        y.append(ps.stem(i))
        
    return " ".join(y)
new['tags']=new['tags'].apply(stem)


from sklearn.feature_extraction.text import CountVectorizer
cv=CountVectorizer(max_features=5000,stop_words='english')
vector=cv.fit_transform(new['tags']).toarray()

from sklearn.metrics.pairwise import cosine_similarity
similarity=cosine_similarity(vector)


def recommend(movie):
    index=new[new['title']==movie].index[0]
    distances=sorted(list(enumerate(similarity[index])),reverse=True,key=lambda x: x[1])
    
    for i in distances[1:6]:
        print(new.iloc[i[0]].title)
        
import pickle
#pickle.dump(new,open("model/movies_list.pkl",'wb'))
#pickle.dump(similarity,open("model/similarity.pkl",'wb'))








