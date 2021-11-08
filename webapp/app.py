from flask import Flask, render_template, request
from flask.json import dump
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
from fuzzywuzzy import process

app = Flask(__name__)
app.secret_key = 'somesecretkeythatonlyishouldknow'

# data
df_movie = pd.read_csv('movies.csv', usecols=['movieId','title'])
df_rating = pd.read_csv('ratings.csv')

movies = df_movie['title']

# preprocessing data
def data_preprocessing(df_rating):
    df_rating = df_rating.drop(['timestamp'], axis=1)
    movies_users=df_rating.pivot(index='movieId', columns='userId'
    ,values='rating').fillna(0)
    m_movies_users=csr_matrix(movies_users.values)
    return m_movies_users


# Recommendation function
def recommend(movie_name, data, recommendations ):
    #model_knn.fit(data)id
    recommendations = recommendations+1
    idx=process.extractOne(movie_name, movies)[2]
    #print('Movie Selected: ',df_rating['title'][idx])#, 'Index: ',id)
    #print('Searching for recommendations.....')
    model_knn = NearestNeighbors(metric = 'cosine', algorithm = 'brute', n_neighbors = 20)
    model_knn.fit(data)
    distances, indices=model_knn.kneighbors(data[idx], n_neighbors = recommendations)
    print (distances)
    titls = []
    for i in indices[0]:
        titls.append(df_movie['title'][i])#.where(i!=idx))
        #print(df_movie['title'][i].where(i!=idx))
    del titls[0]
    return titls

@app.route('/', methods=['POST','GET'])
def home():
    #global recomd
    if request.method == 'POST':
        title = request.form['title_mov']
        data = data_preprocessing(df_rating)
        recomd = recommend(title, data, 5)
        #print(recomd)
    else :
        recomd = ['No movie recommended']
    random_df = df_movie.sample(40)
    titles = random_df.iloc[0:30,1]
    #print(titles)
    context = titles
    res = recomd
    #recomd = recomd
    print('recommended movies : ', res)
    return render_template('index.html', context=context, res = res)
'''
@app.route('/recommended', methods=['POST','GET'])
def recommended():
    
    context = recomd
    return redirect(url_for("designs_list"))
    return render_template('recommand.html', context=context)

'''


if __name__ == '__main__':
   app.run(debug=True)