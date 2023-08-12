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


def get_numeric_input(prompt):
    selected_option_text = st.text_input(prompt)
    selected_option = None

    if selected_option_text:
        try:
            selected_option = float(selected_option_text)
            if 0 <= selected_option <= 1:
                st.write("You selected:", selected_option)
            else:
                st.write("Please enter a value between 0 and 1.")
        except ValueError:
            st.write("Please enter a valid numeric value.")
    
    return selected_option



# Rest of your code...


def calculate_compatibility(user_preferences):
    # Reset compatibility score
    df['compatbilityScore'] = 0 
    df['compatbilityScorePercentage'] = 0 

    # Calculate compatibility score based on user preferences
    for index, row in df.iterrows():
        # print('Before Row : ',row)
        for key, value in user_preferences.items():
            if 'normalized' in key:
                dataset_value = row[key]
                external_value = value
                compact_score  = np.round(1 - np.abs(dataset_value - external_value),2)
                # row['compatbilityScore']+=compact_score
                df.at[index,'compatbilityScore'] +=compact_score
            else:                 
                if key=='age-range':
                    # print('key : ',key)
                    df.at[index,'compatbilityScore']+=2
                elif key== 'FoodChoice':
                    # print('key : ',key)
                    df.at[index,'compatbilityScore']+=2
                elif key=='Smoking':
                    # print('key : ',key)
                    df.at[index,'compatbilityScore']+=2
                elif key=='Drinking':
                    # print('key : ',key)

                    df.at[index,'compatbilityScore']+=2
                elif key=='race':
                    # print('key : ',key)

                    df.at[index,'compatbilityScore']+=2
                elif key=='gender':
                    # print('key : ',key)

                    df.at[index,'compatbilityScore']+=2
                
                elif key=='field':
                    # print('key : ',key)

                    df.at[index,'compatbilityScore']+=2
                    
                
                elif key=='Smoking':
                    # print('key : ',key)
                    df.at[index,'compatbilityScore']+=2
                elif key=='Drinking':
                    # print('key : ',key)

                    df.at[index,'compatbilityScore']+=2


                else:
                    # print('key : ',key)

                    df.at[index,'compatbilityScore']+=1


    # Calculate the maximum compatibility score in the dataset
    max_compatibility_score = len(list(user_preferences.keys()))+9

    # Iterate through the DataFrame and calculate the normalized compatibility score as a percentage
    for index, row in df.iterrows():
        df.at[index,'compatbilityScorePercentage'] = np.round(int((row['compatbilityScore'] / max_compatibility_score) * 100), 2)
    
    compatible_df = df[df['compatbilityScorePercentage'] != 0]
    compatible_df = df.drop_duplicates()
    compatible_df.sort_values(by='compatbilityScorePercentage', ascending=False,inplace=True)
    return compatible_df

df = pd.read_csv('Cleaned_Speed_dating_data.csv')


df = df.drop_duplicates()


st.set_page_config(layout='wide',page_icon='!',page_title='Roommate Compatibility Connection')
path =  os.path.dirname(__file__)
today = date.today()
# Column 1
# Title of the app
st.title("Roommate Compatibility Connection")
st.markdown("Use the options below to select your preferences for finding compatible roommates.")

# Create two columns
col1, col2,col3 = st.columns(3)



with col1:
    
    # Add style to differentiate columns
    st.markdown("<style>div[role='listbox'] { background-color: #f2f2f2; padding: 5px; }</style>", unsafe_allow_html=True)
    
    # Dropdown menu
    selected_option_age = st.selectbox("Select an option for Age :", sorted(df['age-range'].unique().tolist()))
    # Display the selected option
    st.write("You selected:", selected_option_age)

    selected_option_gender = st.selectbox("Select an option for Gender :", df['gender'].unique().tolist())
    # Display the selected option
    st.write("You selected:", selected_option_gender)

    selected_option_race = st.selectbox("Select an option for Ethnicity :", df['race'].unique().tolist())
    # Display the selected option
    st.write("You selected:", selected_option_race)

    selected_option_field = st.selectbox("Select an option for Field :", df['field'].unique().tolist())
    # Display the selected option
    st.write("You selected:", selected_option_field)

    selected_option_food = st.selectbox("Select an option for Food Habit :", df['FoodChoice'].unique().tolist())
    # Display the selected option
    st.write("You selected:", selected_option_food)
    
    selected_option_smooking = st.selectbox("Select an option for Smooking Habit :", df['Smoking'].unique().tolist())
    # Display the selected option
    st.write("You selected:", selected_option_smooking)
    
    selected_option_drinking = st.selectbox("Select an option for Alcohol Consumption :", df['Drinking'].unique().tolist())
    # Display the selected option   
    st.write("You selected:", selected_option_drinking)
    
    selected_option_religion = get_numeric_input("Select an option for Religion Faith & Belief (Preference order(0-1)):")   

    

with col2:

    selected_option_reading = get_numeric_input("Select an option for Academic (Preference order(0-1)):")   
    selected_option_gaming = get_numeric_input("Select an option for Gaming Habit(Preference order(0-1)):")   
    selected_option_movie = get_numeric_input("Select an option for Movie lover(Preference order(0-1)):")   
    selected_option_sports = get_numeric_input("Select an option for Sports Enthusiasm(Preference order(0-1)):")   
    selected_option_music = get_numeric_input("Select an option for Music Lover(Preference order(0-1)):")   
    selected_option_dining = get_numeric_input("Select an option for Eating Ritual(Preference order(0-1)):")
    
    selected_option_tv = get_numeric_input("Select an option for Binge-Watching (Preference order(0-1)):")   
    selected_option_clubbing = get_numeric_input("Select an option for party & Clubbing(Preference order(0-1)):")   
    selected_option_hiking = get_numeric_input("Select an option for Trip & Hiking(Preference order(0-1)):")   
    selected_option_exercise = get_numeric_input("Select an option for Exercise and yoga(Preference order(0-1):")   
   
 
  
selected_option_origon_location = st.text_input("Enter Your University/office/Home location:")
# Display the entered text
st.write("You entered:", selected_option_origon_location)

if selected_option_origon_location:
    
    if st.button('Calculate Compatibility'):

        user_preferences = {'age-range': selected_option_age,
                    'gender': selected_option_gender,
                    'race': selected_option_race,
                    'field': selected_option_field,
                    'Smoking':selected_option_smooking,
                    'Drinking':selected_option_drinking,
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
        # print(user_preferences)
        # st.dataframe( pd.DataFrame.from_dict(user_preferences))
        compatibility_df = calculate_compatibility(user_preferences)
        # st.dataframe(compatibility_df)            
      
        st.title("Available Roommates - Sorted by Compatibility Score")
        col1,col2 = st.columns(2)

        with col1:

            compatible_sorted_df = compatibility_df.head()
            # st.dataframe(compatible_sorted_df) 
            # st.dataframe(compatible_sorted_df)            

            for index,row in compatible_sorted_df.iterrows():
                distance = get_distance(row['locations'], selected_option_origon_location)
                if distance:
                    st.markdown(
                        f"""
                        <div style="background-color: #f9f9f9; padding: 15px; border-radius: 15px; box-shadow: 2px 2px 5px #888888;">
                        <h3>Name- XYZ-{index} </h3>
                        <h5>Distance between {row['locations']} - {selected_option_origon_location} : {distance/1000}-KM</h5>
                        <h5><strong>Compatibility Score:</strong> {row['compatbilityScorePercentage']}%</h5>
                        <table border="0">
                            <tr>
                                <td><strong>Age Range:</strong> {row['age-range']}</td>
                                <td><strong>Gender:</strong> {row['gender']}</td>
                                <td><strong>Race:</strong> {row['race']}</td>
                            </tr>
                            <tr>
                                <td><strong>Field of Interest:</strong> {row['field']}</td>
                                <td><strong>Academic and Reading Preference:</strong> {row['reading_normalized']}</td>
                                <td><strong>Gaming Habit :</strong> {row['gaming_normalized']}</td>
                            </tr>
                            <tr>
                                <td><strong>Music Lover:</strong> {row['music_normalized']}</td>
                                <td><strong>Eating Ritual :</strong> {row['dining_normalized']}</td>
                                <td><strong>Location :</strong> {row['locations']}</td>
                            </tr>
                            <tr>
                                <td><strong>Movie Lover:</strong> {row['movies_normalized']}</td>
                                <td><strong>Binge-Watching:</strong> {row['tv_normalized']}</td>
                                <td><strong>Party and Clubbing :</strong> {row['clubbing_normalized']}</td>
                            </tr>
                            <tr>
                                <td><strong>Trip & Hiking :</strong> {row['hiking_normalized']}</td>
                                <td><strong>Exercise and Yoga :</strong> {row['exercise_normalized']}</td>
                                <td><strong>Sports Enthusiasm :</strong> {row['sports_normalized']}</td>
                            </tr>
                            <tr>
                                <td><strong>Religion Faith & belief :</strong> {row['importance_same_religion_normalized']}</td>
                                <td><strong>Food Habit :</strong> {row['FoodChoice']}</td> 
                                <td><strong>Smooking Habit :</strong> {row['Smoking']}</td>
                            </tr>
                            <tr>
                                <td><strong>Alcohol Consumption :</strong> {row['Drinking']}</td>   
                            </tr> 
                            
                            
                        </table>
                            
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
        with col2:
            
            compatible_sorted_df = compatibility_df.head()
            for index,row in compatible_sorted_df.iterrows():
                distance = get_distance(row['locations'], selected_option_origon_location)

                if distance:
                    st.markdown(
                        f"""
                        <div style="background-color: #f9f9f9; padding: 15px; border-radius: 15px; box-shadow: 2px 2px 5px #888888;">
                        <h3>Name- XYZ-{index} </h3>
                        <h5>Distance between {row['locations']} - {selected_option_origon_location} : {distance/1000}-KM</h5>
                        <h5><strong>Compatibility Score:</strong> {row['compatbilityScorePercentage']}% </h5>
                        <h5><strong>Location :</strong> {row['locations']}</h5>

                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    