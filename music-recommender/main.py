
import pandas as pd
import numpy as np
import pickle

# Load dataset
df = pd.read_csv("ex.csv")

# Remove null values
df.dropna(inplace=True)

# Remove duplicates
df = df.drop_duplicates()

# Clean User-Rating
l = []
for i in df["User-Rating"]:
    l.append(str(i)[:3])

df["User-Rating"] = l

# Clean text columns
df['Album/Movie'] = df['Album/Movie'].str.replace(' ', '')
df['Singer/Artists'] = df['Singer/Artists'].str.replace(' ', '')
df['Singer/Artists'] = df['Singer/Artists'].str.replace(',', '')

# Create tags
df['tags'] = df['Singer/Artists'] + ' ' + df['Genre'] + ' ' + df['Album/Movie'] + ' ' + df['User-Rating']

# Final dataframe
new_df = df[['Song-Name', 'tags']].copy()

# Rename column
new_df.rename(columns={'Song-Name': 'title'}, inplace=True)

# Vectorization
from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features=2000, stop_words='english')
vectors = cv.fit_transform(new_df['tags']).toarray()

# Similarity
from sklearn.metrics.pairwise import cosine_similarity
similarity = cosine_similarity(vectors)

# Test
def recommend(music):
    music_index = new_df[new_df['title'] == music].index[0]
    distance = similarity[music_index]
    music_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]

    for i in music_list:
        print(new_df.iloc[i[0]].title)

recommend('Proper Patola')

# Save files
pickle.dump(new_df, open('musirec.pkl', 'wb'))
pickle.dump(similarity, open('similarities.pkl', 'wb'))