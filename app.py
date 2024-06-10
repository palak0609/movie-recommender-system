import streamlit as st
import pickle
import pandas as pd
import requests


# Function to set custom styles
def set_styles():
    styles = """
    <style>
    .reportview-container {
        background-color: #F2F607;              /* yellow background for main content */
    }
    .sidebar .sidebar-content {
        background-color: #0E1673;              /* dark blue background for sidebar */
    }
    .stSelectbox label {
        color: #4a4a4a;                         /* grey color for selectbox label */
        font-size: 20px;
        font-weight: bold;
    }
    .stButton button {
        background-color: #4769A0;             /* blue dark background for buttons */
        color: #000000;                          /* black text for buttons */
        font-size: 16px;
        font-weight: bold;
        border-radius: 10px;
        display: block;
        margin-left: auto;
        margin-right: auto;
    }
    .stButton button:hover {
        background-color: #243E68;             /* Darker blue background for button hover state */
        color: #000000;                         /* Black text for buttons */
    }
    .movie-title {
        font-size: 15px;
        font-weight: bold;
        color: #2C813C;                               /* dark green color for movie titles */
        text-align: center;
    }
    .recommendation {
        border: 2px solid #ECFF00;                   /* bright yellow border for recommendation boxes */     
        border-radius: 10px;
        padding: 5px;
        background-color: #FFFFFF;                      /* White background for recommendation boxes */
        margin-bottom: 5px;
    }
    .centered-title {
        font-size: 36px;
        font-weight: bold;
        color: #FFFFFF;                               /* Black color for title */
        text-align: center;
        margin-top: 0;
        margin-bottom: 0;
    }
    </style>
    """
    st.markdown(styles, unsafe_allow_html=True)


set_styles()


def fetch_poster(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=7c11f3be7be57705976bc806c5a3aa1b'.format(movie_id))
    # we need to convert response to json
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity_matrix[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        # to fetch id for poster extraction
        # fetch posters from API
        # we will print the name of the movie
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters


movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity_matrix = pickle.load(open('similarity.pkl', 'rb'))

# Center the title
st.markdown("<h1 class='centered-title'>Movie Recommender System</h1>", unsafe_allow_html=True)

selected_movie_name = st.selectbox(
    'Search for your favourite movies to binge watch >3',
    movies['title'].values)

if st.button('Recommend'):
    with st.spinner('Fetching recommendations..'):
        names, posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)
    for i, col in enumerate([col1, col2, col3, col4, col5]):
        with col:
            st.markdown(
                f'<div class="recommendation"><p class="movie-title">{names[i]}</p><img src="{posters[i]}" width="100%"></div>',
                unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
