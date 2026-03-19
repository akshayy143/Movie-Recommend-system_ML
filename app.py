import requests
import streamlit as st
import numpy as np
import pickle
import pandas as pd
import requests


# Set page to wide mode for better OTT experience
st.set_page_config(layout="wide", page_title="MovieFlix")

# Custom CSS for Movie Cards
st.markdown("""
    <style>
    .movie-card {
        border-radius: 10px;
        transition: transform .2s;
    }
    .movie-card:hover {
        transform: scale(1.05);
    }
    .stButton>button {
        background-color: #E50914;
        color: white;
        width: 100%;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Inject Netflix CSS
st.markdown("""
    <style>
    /* Main background */
    .stApp {
        background-color: #141414;
    }

    /* Header styling */
    h1 {
        color: #E50914; /* Netflix Red */
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-weight: bold;
        font-size: 3rem !important;
    }

    /* Selection box styling */
    .stSelectbox div[data-baseweb="select"] {
        background-color: #333;
        color: white;
    }

    /* Movie Title Text */
    .movie-title {
        color: #e5e5e5;
        font-size: 14px;
        font-weight: 500;
        text-align: center;
        margin-top: 5px;
    }

    /* Poster Hover Effect */
    .stImage img {
        border-radius: 4px;
        transition: transform .3s;
    }
    .stImage img:hover {
        transform: scale(1.08);
        cursor: pointer;
    }
    </style>
    """, unsafe_allow_html=True)


# def fetch_poster(movie_id):
#     response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'.format(movie_id))
#     data = response.json()
#     return "http://image.tmdb.org/t/p/w500/" + data['poster_path']

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    try:
        # Added a 5-second timeout
        response = requests.get(url, timeout=5)
        response.raise_for_status() # Check if the request was successful
        data = response.json()
        poster_path = data['poster_path']
        # full_path = "https://image.tmdb.org" + poster_path
        full_path = "https://picsum.photos/400/300?random=2" + poster_path
        return full_path
    except Exception as e:
        # Return a placeholder image if the API fails
        # return "https://via.placeholder.com"
        return "https://picsum.photos/400/300?random=2"




def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []

    for  i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id

        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies , recommended_movies_posters

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))



st.title('🎬 MovieFlix Recommendations')
st.write("Find your next favorite movie based on what you love.")

selected_movie_name = st.selectbox(
    'Select Movie Name',
    movies['title'].values)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)


    col1, col2, col3,col4,col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image("https://picsum.photos/400/300?random=2")

    with col2:
        st.text(names[1])
        st.image("https://picsum.photos/400/300?random=4")

    with col3:
        st.text(names[2])
        st.image("https://picsum.photos/400/300?random=1")

    with col4:
        st.text(names[3])
        st.image("https://picsum.photos/400/300?random=3")
    with col5:
        st.text(names[4])
        st.image("https://picsum.photos/400/300?random=5")


