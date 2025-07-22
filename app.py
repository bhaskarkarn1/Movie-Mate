import pickle
import pandas as pd
import streamlit as st
import requests

# Load pre-uploaded pickle files
movies_dict = pickle.load(open('models/movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('models/similarity.pkl', 'rb'))

# Fetch poster from TMDB API
def fetch_poster(movie_id):
    response = requests.get(
        f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=c988694dfb23ccc5a55ac82f632288b0&language=en-US'
    )
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

# Recommendation logic
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_posters

# Streamlit UI
st.title('🎬 Movie Mate')

selected_movie = st.selectbox(
    'Which movie do you want to look at?',
    movies['title'].values
)

if st.button('Recommend'):
    names, posters = recommend(selected_movie)
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.image(posters[i], use_container_width=True)
            st.markdown(
                f"<p style='text-align:center; font-weight:bold;'>{names[i]}</p>",
                unsafe_allow_html=True
            )
