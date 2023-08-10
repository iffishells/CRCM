import streamlit as st
import pandas as pd
import numpy as np
import warnings
from datetime import date
import os
import glob
import requests
import math

warnings.simplefilter(action='ignore',category=FutureWarning)


def normalize_values(df,current_feature_name ,current_scaled_feature_name , new_feature_name):
    temp = df.copy()  # Create a copy of the DataFrame to avoid modifying the original
    temp[new_feature_name] = 0  # Add a new column to store normalized values
    
    for index, row in temp.iterrows():
        yoda = row[current_feature_name]
        scale_yoga = int(row[current_scaled_feature_name].split(']')[0].split('-')[-1])
        yoga_normalized = yoda / scale_yoga
        temp.loc[index, new_feature_name] = yoga_normalized
    
    return temp


def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of the Earth in kilometers

    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c
    return distance
def get_coordinates(api_key, city_name):
    base_url = "https://atlas.microsoft.com/search/address/json"
    params = {
        "api-version": "1.0",
        "subscription-key": api_key,
        "query": city_name
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    if "results" in data and data["results"]:
        location = data["results"][0]["position"]
        latitude = location["lat"]
        longitude = location["lon"]
        return latitude, longitude
    else:
        return None, None
    
def get_distance(from_city_name,to_city_name):
    
    api_key = "szf6w7lIXw-H0uNVASqmK2TqlaNO-LRXXbt91ODbEb8"
    from_latitude, from_longitude = get_coordinates(api_key, from_city_name)
    to_latitude, to_longitude = get_coordinates(api_key, to_city_name)
    
    # if from_latitude is not None and from_longitude is not None:
    #     print(f"Coordinates for {from_city_name}: Latitude={from_latitude}, Longitude={from_longitude}")
    # else:
    #     print(f"Coordinates not found for {from_city_name}")

    # if to_latitude is not None and to_longitude is not None:
    #     print(f"Coordinates for {to_city_name}: Latitude={to_latitude}, Longitude={to_longitude}")
    # else:
    #     print(f"Coordinates not found for {to_city_name}")

    distance = haversine_distance(from_latitude, from_longitude, to_latitude, to_longitude)
    # print(f"Distance between the cities: {distance:.2f} km")
    
    return np.round(distance,2)

def calculate_compatibility(user_preferences):
    # Reset compatibility score
    df['compatbilityScore'] = 0 
    df['compatbilityScorePercentage'] = 0 

    # Calculate compatibility score based on user preferences
    for index, row in df.iterrows():
        for key, value in user_preferences.items():
            if row[key] == value:
                df.at[index, 'compatbilityScore'] += 1
    
    # Calculate the maximum compatibility score in the dataset
    max_compatibility_score = len(list(user_preferences.keys()))

    # Iterate through the DataFrame and calculate the normalized compatibility score as a percentage
    for index, row in df.iterrows():
        df.at[index, 'compatbilityScorePercentage'] = np.round(int((row['compatbilityScore'] / max_compatibility_score) * 100), 2)
    
    compatible_df = df[df['compatbilityScorePercentage'] != 0]

    for index, row in compatible_df.iterrows():
            compatible_df.at[index, 'compatbilityScorePercentage'] = np.round(int((row['compatbilityScore'] / max_compatibility_score) * 100),2)

    compatible_df.sort_values(by='compatbilityScorePercentage', ascending=False,inplace=True)
    return compatible_df


df = pd.read_csv('CleadedSpeedDatingData.csv') 
df.reset_index(inplace=True)



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
    st.markdown("<style>div[role='listbox'] { background-color: #f2f2f2; padding: 5px; }</style>", unsafe_allow_html=True)
    
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
    selected_option_food = st.selectbox("Select an option for Food Choice :", df['FoodChoice'].unique().tolist())
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

  
selected_option_origon_location = st.text_input("Enter Your University/office/Home location:")
# Display the entered text
st.write("You entered:", selected_option_origon_location)

if selected_option_origon_location:
    if st.button('Calculate Compatibility'):
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
                    'importance_same_religion_normalized':selected_option_religion,
                    'FoodChoice':selected_option_food

                }


        compatibility_df = calculate_compatibility(user_preferences)
               
        st.title("Available Roommates - Sorted by Compatibility Score")
        col1,col2 = st.columns(2)

        with col1:
            st.dataframe(compatibility_df)            

            compatible_sorted_df = compatibility_df.head()
            # st.dataframe(compatible_sorted_df) 
            st.dataframe(compatible_sorted_df)            

            for index,row in compatible_sorted_df.iterrows():
                distance = get_distance(row['locations'], selected_option_origon_location)
                if distance:
                    st.markdown(
                        f"""
                        <div style="background-color: #f9f9f9; padding: 15px; border-radius: 15px; box-shadow: 2px 2px 5px #888888;">
                        <h3>Name- XYZ </h3>
                        <h5>Distance between {row['locations']} - {selected_option_origon_location} : {distance}-KM</h5>
                        <table border="0">
                            <tr>
                                <td><strong>Age Range:</strong> {row['age-range']}</td>
                                <td><strong>Gender:</strong> {row['gender']}</td>
                                <td><strong>Race:</strong> {row['race']}</td>
                            </tr>
                            <tr>
                                <td><strong>Field of Work:</strong> {row['field']}</td>
                                <td><strong>Compatibility Score:</strong> {row['compatbilityScorePercentage']}</td>
                                <td><strong>Reading Habit:</strong> {row['reading_normalized']}</td>
                            </tr>
                            <tr>
                                <td><strong>Gaming Habit :</strong> {row['gaming_normalized']}</td>
                                <td><strong>Music Listening Habit :</strong> {row['music_normalized']}</td>
                                <td><strong>Dining Habit :</strong> {row['dining_normalized']}</td>
                            </tr>
                            <tr>
                                <td><strong>Wactching Moies :</strong> {row['movies_normalized']}</td>
                                <td><strong>Watching TV :</strong> {row['tv_normalized']}</td>
                                <td><strong>clubbing :</strong> {row['clubbing_normalized']}</td>
                            </tr>
                            <tr>
                                <td><strong>Hiking :</strong> {row['hiking_normalized']}</td>
                                <td><strong>Exercise Habit :</strong> {row['exercise_normalized']}</td>
                                <td><strong>Sports Habit :</strong> {row['sports_normalized']}</td>
                            </tr>
                            <tr>
                                <td><strong>Importance of same religion Level :</strong> {row['importance_same_religion_normalized']}</td>
                                <td><strong>Food choice :</strong> {row['FoodChoice']}</td>
                                <td><strong>Location :</strong> {row['locations']}</td>
                            </tr>
                            
                            
                        </table>
                            
                        </div>
                        """,
                        unsafe_allow_html=True
                    )