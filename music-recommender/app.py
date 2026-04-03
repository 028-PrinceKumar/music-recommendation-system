import streamlit as st
import pickle
import pandas as pd
import requests
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

music_path = os.path.join(BASE_DIR, 'musirec.pkl')
similarity_path = os.path.join(BASE_DIR, 'similarity.pkl')   # <-- make sure file name is this


music_dict = pickle.load(open(music_path, 'rb'))
music = pd.DataFrame(music_dict)

similarity = pickle.load(open(similarity_path, 'rb'))


def fetch_poster(music_title):
    try:
        url = f"https://saavn.sumit.co/api/search/songs?query={music_title}"
        response = requests.get(url, timeout=10)
        data = response.json()
        poster_url = data['data']['results'][0]['image'][2]['link']
        return poster_url
    except:
        return "https://via.placeholder.com/300x300?text=No+Image"


def recommend(musics):
    music_index = music[music['title'] == musics].index[0]
    distances = similarity[music_index]

    music_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_music = []
    recommended_music_poster = []

    for i in music_list:
        music_title = music.iloc[i[0]].title
        recommended_music.append(music_title)
        recommended_music_poster.append(fetch_poster(music_title))

    return recommended_music, recommended_music_poster


st.title(' Music Recommendation System')

selected_music_name = st.selectbox(
    'Select a music you like',
    music['title'].values
)

if st.button('Recommend'):
    names, posters = recommend(selected_music_name)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])

    with col4:
        st.text(names[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])
