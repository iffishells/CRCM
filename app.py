import streamlit as st
import pandas as pd
import numpy as np
import warnings
from datetime import date
import os
import glob
warnings.simplefilter(action='ignore',category=FutureWarning)


def normalize_values(df,current_feature_name ,current_scaled_feature_name , new_feature_name):
    # current_feature_name = 'yoga'
    # current_scaled_feature_name = 'd_yoga'
    # new_feature_name = 'yoga_normalized'
    temp = df.copy()  # Create a copy of the DataFrame to avoid modifying the original
    temp[new_feature_name] = 0  # Add a new column to store normalized values
    
    for index, row in temp.iterrows():
        yoda = row[current_feature_name]
        scale_yoga = int(row[current_scaled_feature_name].split(']')[0].split('-')[-1])
        yoga_normalized = yoda / scale_yoga
        temp.loc[index, new_feature_name] = yoga_normalized
    
    return temp

df = pd.read_csv('CleadedSpeedDatingData.csv') 
df.reset_index(inplace=True)
df['compatbilityScore'] = 0 

st.set_page_config(layout='wide',page_icon='!',page_title='Roomate Compactibility Tests')
path =  os.path.dirname(__file__)
today = date.today()
# Column 1
# Title of the app
st.title("Roomate Compactibility Tests")
st.markdown("Use the options below to select your preferences for finding compatible roommates.")

# Create two columns
col1, col2,col3 = st.columns(3)



with col1:
    
    # Add style to differentiate columns
    st.markdown("<style>div[role='listbox'] { background-color: #f2f2f2; padding: 10px; }</style>", unsafe_allow_html=True)
    
    # Dropdown menu
    selected_option_age = st.selectbox("Select an option for Age :", df['age-range'].unique().tolist())
    # Display the selected option
    st.write("You selected:", selected_option_age)

    selected_option_gender = st.selectbox("Select an option for Gender :", df['gender'].unique().tolist())
    # Display the selected option
    st.write("You selected:", selected_option_gender)

    selected_option_race = st.selectbox("Select an option for race :", df['race'].unique().tolist())
    # Display the selected option
    st.write("You selected:", selected_option_race)

    selected_option_field = st.selectbox("Select an option for Field :", df['field'].unique().tolist())
    # Display the selected option
    st.write("You selected:", selected_option_field)


    selected_option_music = st.selectbox("Select an option for Music Listening Habit(Preference order(0-1)) :", df['music_normalized'].unique().tolist())
    # Display the selected option
    st.write("You selected:", selected_option_music)

    selected_option_dining = st.selectbox("Select an option for Eating Dining Habit(Preference order(0-1)) :", df['dining_normalized'].unique().tolist())
    # Display the selected option
    st.write("You selected:", selected_option_dining)
    


   

    # # Add a line break
    # st.markdown("<br>", unsafe_allow_html=True)
with col2:
    selected_option_reading = st.selectbox("Select an option for Reading Habit(Preference order(0-1)) :", df['reading_normalized'].unique().tolist())
    # Display the selected option
    st.write("You selected:", selected_option_reading)

    selected_option_gaming = st.selectbox("Select an option for Gaming Habit(Preference order(0-1)) :", df['gaming_normalized'].unique().tolist())
    # Display the selected option
    st.write("You selected:", selected_option_gaming)

    selected_option_movie = st.selectbox("Select an option for Watching Movie(Preference order(0-1)) :", df['movies_normalized'].unique().tolist())
    # Display the selected option
    st.write("You selected:", selected_option_movie)
    
    selected_option_sports = st.selectbox("Select an option for Sports Habit(Preference order(0-1)) :", df['sports_normalized'].unique().tolist())
    # Display the selected option
    st.write("You selected:", selected_option_sports)
    selected_option_food = st.selectbox("Select an option for Sports Habit(Preference order(0-1)) :", df['FoodChoice'].unique().tolist())
    # Display the selected option
    st.write("You selected:", selected_option_food)


  

with col3:
    
    selected_option_tv = st.selectbox("Select an option for Watching TV (Preference order(0-1)) :", df['tv_normalized'].unique().tolist())
    # Display the selected option
    st.write("You selected:", selected_option_tv)

    selected_option_clubbing = st.selectbox("Select an option for Clubbing(Preference order(0-1)) :", df['clubbing_normalized'].unique().tolist())
    # Display the selected option
    st.write("You selected:", selected_option_clubbing)

    selected_option_hiking = st.selectbox("Select an option for Hiking Habit(Preference order(0-1)) :", df['hiking_normalized'].unique().tolist())
    # Display the selected option
    st.write("You selected:", selected_option_hiking)
    
    selected_option_exercise = st.selectbox("Select an option for Exercise Habit(Preference order(0-1)) :", df['exercise_normalized'].unique().tolist())
    # Display the selected option
    st.write("You selected:", selected_option_exercise)

    selected_option_religion = st.selectbox("Select an option for Importance of Same Religion(0-1)) :", df['importance_same_religion_normalized'].unique().tolist())
    # Display the selected option
    st.write("You selected:", selected_option_religion)

  



user_preferences = {'age-range': selected_option_age,
                'gender': selected_option_gender,
                'race': selected_option_race,
                'field': selected_option_field,
                'reading_normalized':selected_option_reading,
                'gaming_normalized':selected_option_gaming,
                'music_normalized':selected_option_music,
                'dining_normalized':selected_option_dining,
                'movies_normalized':selected_option_movie,
                'tv_normalized':selected_option_tv,
                'clubbing_normalized':selected_option_clubbing,
                'hiking_normalized':selected_option_hiking,

                'exercise_normalized':selected_option_exercise,
                'sports_normalized':selected_option_sports,
                'importance_same_religion_normalized':selected_option_religion
            }

interested_records = []
for index , row in df.iterrows():
    # logging.info(f'Iterating row number {index}')
    for key,value in user_preferences.items():
        if row[key]== user_preferences[key]:
            
            df.loc[index,'compatbilityScore'] +=1
            interested_records.append(index)
            
            
            
                     # <img src="path_to_signal_image.png" alt="Signal Image" width="300">

# Calculate the maximum compatibility score in the dataset
max_compatibility_score = df['compatbilityScore'].max()
# Iterate through the DataFrame and calculate the normalized compatibility score as a percentage
for index, row in df.iterrows():
    df.loc[index, 'compatbilityScore'] = np.round(int((row['compatbilityScore'] / max_compatibility_score) * 100),2)
               
compatible_df = df[df['compatbilityScore'] != 0][['age-range','gender','race','field','compatbilityScore']]
compatible_sorted_df = compatible_df.sort_values(by='compatbilityScore', ascending=False)
# st.title("Available Roommates - Sorted by Compatibility Score")
# styled_sorted_df = compatible_sorted_df.style.set_properties(**{'background-color': 'white', 'color': 'black'})
# st.dataframe(styled_sorted_df)
col1,col2 = st.columns(2)
with col1:
    
    compatible_df = compatible_df.head()
    for index,row in compatible_df.iterrows():
        st.markdown(
            f"""
            <div style="background-color: #f9f9f9; padding: 15px; border-radius: 15px; box-shadow: 2px 2px 5px #888888;">
                <h3>Name- XYZ </h3>
                <p><strong>Age Range :</strong> {row['age-range']}</p>
                <p><strong>Gender :</strong> {row['gender']}</p>
                <p><strong>Race :</strong> {row['race']}</p>
                <p><strong>field of work :</strong> {row['field']}</p>
                <p><strong>compatbilityScore:</strong>{row['compatbilityScore']} </p>
                <p><strong>Description:</strong> This is a sample signal with some information.</p>
            </div>
            """,
            unsafe_allow_html=True
        )