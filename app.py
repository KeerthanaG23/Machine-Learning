# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 09:21:56 2023

@author: Keerthana
"""


from flask import Flask, request, render_template, request,redirect,url_for
import requests
import pandas as pd
from patsy import dmatrices
import mysql.connector
import hashlib
import pymysql as pms
import pickle
#%%
app = Flask(__name__)
#@app.route('/')
#def home():
#    return render_template("index.html")
#%%
@app.route('/')
def home():
    return render_template("login.html")
#%%
conn=pms.connect(host='localhost',
                 port=3306,
                 user='root',
                 password='Kethysahan04',
                 )
cursor=conn.cursor()
#cursor.execute("CREATE DATABASE dbasemlt1;")
cursor.execute("USE dbasemlt1")
cursor.execute('SELECT * FROM accounts' )
output=cursor.fetchall()

#%%

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = 'invalid username or password'
    # Check if "username" and "password" POST requests exist (user submitted form)
    #print("hello2")
   # if request.method == 'POST' and 'full-name' in request.form and 'password' in request.form:
    # Create variables for easy access
    username = request.form['full-name']
    password = request.form['password']
    cursor.execute('SELECT * FROM accounts WHERE username = %s AND pass = %s', (username, password))
    account = cursor.fetchone()
    print(username,password)
    print(account)
    if account:
        return redirect(url_for('index'))
    else:
        msg = 'Incorrect username/password!'
        return render_template('login.html', msg=msg)
    return render_template('login.html', msg=msg)


@app.route('/index')
def index():
    return render_template("index.html")

#%%
@app.route('/index')
def hom():
    return render_template("index.html")




#%%
movies = pickle.load(open('model/movies_list.pkl','rb'))
similarity=pickle.load(open('model/similarity.pkl','rb'))

#%%
def fetch_poster(movie_id):
    #url="https://api.themoviedb.org/3/movie/{}?api_key=THE_KEY&language=en-US".format(movie_id)
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data=requests.get(url)
    data=data.json()
    poster_path=data['poster_path']
    full_path="https://image.tmdb.org/t/p/w500/"+poster_path
    return full_path

#%%
def recommend(movie):
    index=movies[movies['title']==movie].index[0]
    distances= sorted(list(enumerate(similarity[index])),reverse=True,key=lambda x:x[1])
    recommended_movies_name=[]
    recommended_movies_poster=[]
    for i in distances[1:6]:
        movie_id=movies.iloc[i[0]].movie_id
        recommended_movies_poster.append(fetch_poster(movie_id))
        recommended_movies_name.append(movies.iloc[i[0]].title)
        
    return recommended_movies_name,recommended_movies_poster



@app.route('/about.html')
def about():
    return render_template("about.html")

@app.route('/prediction',methods=['GET'])
def prediction():
    movie_list=movies['title'].values
    status=False
    return render_template("prediction.html",movie_list=movie_list,status=status)
    
@app.route('/submit', methods=['GET'])
def submit():
    movie_list=movies['title'].values
    movies_name=request.args.get('movies')
    #movies_name=request.form.get('movies')
    print(movies_name)
    recommended_movies_name,recommended_movies_poster=recommend(movies_name)
    print(recommended_movies_name)
    print(recommended_movies_poster)
    status=True
    return render_template("prediction.html",movies_name=recommended_movies_name,poster=recommended_movies_poster,movie_list=movie_list,status=status)
#%%
if __name__=='__main__':
    app.run(host='localhost',port=5000)
