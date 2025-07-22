import pickle
import pandas as pd
import streamlit as st
import requests
import os
import urllib.request

# Create a folder to store the downloaded files
if not os.path.exists("models"):
    os.makedirs("models")

# Download movie_dict.pkl
movie_dict_url = "https://drive.google.com/uc?id=13zleeD7zwLRLHI0VMxBbFVGOm8R4pdcb"
urllib.request.urlretrieve(movie_dict_url, "models/movie_dict.pkl")

# Download similarity.pkl
similarity_url = "https://drive.google.com/uc?id=19-LunxNRbAIrwRpaOfmlBpV7D1LAgypR"
urllib.request.urlretrieve(similarity_url, "models/similarity.pkl")

# Load data
movies_dict = pickle.load(open('models/movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('models/similarity.pkl', 'rb'))

# TMDB Poster Fetch Function
def fetch_poster(movie_id):
    response = requests.get(
        f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=c988694dfb23ccc5a55ac82f632288b0&language=en-US'
    )
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

# Recommendation Function
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

# UI
st.title('🎬 Movie Mate')

selected_movie_name = st.selectbox(
    'Which movie do you want to look at?',
    movies['title'].values
)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.image(posters[i], use_container_width=True)
            st.markdown(
                f"<p style='text-align:center; font-weight:bold;'>{names[i]}</p>",
                unsafe_allow_html=True
            )
