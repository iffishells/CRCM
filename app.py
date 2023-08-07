import streamlit as st
import pandas as pd
import numpy as np

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

df = pd.read_csv('speed-dating_csv.csv') 
df  =  df[df['has_null']==0]
df = normalize_values(df,'yoga','d_yoga','yoga_normalized')
df = normalize_values(df,'shopping','d_shopping','shopping_normalized')
df = normalize_values(df,'concerts','d_concerts','concerts_normalized')
df = normalize_values(df,'theater','d_theater','theater_normalized')
df = normalize_values(df,'reading','d_reading','reading_normalized')

df = normalize_values(df,'gaming','d_gaming','gaming_normalized')
df = normalize_values(df,'art','d_art','art_normalized')
df = normalize_values(df,'dining','d_dining','dining_normalized')
df = normalize_values(df,'music','d_music','music_normalized')
df = normalize_values(df,'movies','d_movies','movies_normalized')
df = normalize_values(df,'tv','d_tv','tv_normalized')
df = normalize_values(df,'clubbing','d_clubbing','clubbing_normalized')
df = normalize_values(df,'hiking','d_hiking','hiking_normalized')
df = normalize_values(df,'museums','d_museums','museums_normalized')
df = normalize_values(df,'exercise','d_exercise','exercise_normalized')
df = normalize_values(df,'sports','d_sports','sports_normalized')
df = normalize_values(df,'tvsports','d_tvsports','tvsports_normalized')
df = normalize_values(df,'intelligence','d_intelligence','intelligence_normalized')
df = normalize_values(df,'sincere','d_sincere','sincere_normalized')
df = normalize_values(df,'ambition','d_ambition','ambition_normalized')
df = normalize_values(df,'funny','d_funny','funny_normalized')
df = normalize_values(df,'attractive','d_attractive','attractive_normalized')


df.reset_index(inplace=True)
df['compatbilityScore'] = 0 


# Column 1
# Title of the app
st.title("Roomate Compactibility Testssss")
st.markdown("Use the options below to select your preferences for finding compatible roommates.")

# Create two columns
col1, col2,col3 = st.columns(3)



with col1:
    
    # Add style to differentiate columns
    st.markdown("<style>div[role='listbox'] { background-color: #f2f2f2; padding: 10px; }</style>", unsafe_allow_html=True)
    
    # Dropdown menu
    selected_option_age = st.selectbox("Select an option for Age :", df['age'].unique().tolist())
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

    selected_option_yoga = st.selectbox("Select an option for Yoga(Preference order(0-1)) :", df['yoga_normalized'].unique().tolist())
    # Display the selected option
    st.write("You selected:", selected_option_yoga)
    
    selected_option_art = st.selectbox("Select an option for Artist Personality(Preference order(0-1)) :", df['art_normalized'].unique().tolist())
    # Display the selected option
    st.write("You selected:", selected_option_art)

    selected_option_music = st.selectbox("Select an option for Music Listening Habit(Preference order(0-1)) :", df['music_normalized'].unique().tolist())
    # Display the selected option
    st.write("You selected:", selected_option_music)

    selected_option_dining = st.selectbox("Select an option for Eating Dining Habit(Preference order(0-1)) :", df['dining_normalized'].unique().tolist())
    # Display the selected option
    st.write("You selected:", selected_option_dining)
    
    selected_option_meseums = st.selectbox("Select an option for Museums Habit(Preference order(0-1)) :", df['museums_normalized'].unique().tolist())
    # Display the selected option
    st.write("You selected:", selected_option_meseums)

   

    # # Add a line break
    # st.markdown("<br>", unsafe_allow_html=True)
with col2:
        
    selected_option_shopping  = st.selectbox("Select an option for Shopping Habit(Preference order(0-1)) :", df['shopping_normalized'].unique().tolist())
    # Display the selected option
    st.write("You selected:", selected_option_shopping)


    selected_option_concert = st.selectbox("Select an option for Concerts Habit(Preference order(0-1)) :", df['concerts_normalized'].unique().tolist())
    # Display the selected option
    st.write("You selected:", selected_option_concert)


    selected_option_theater = st.selectbox("Select an option for Theater Habit(Preference order(0-1)) :", df['theater_normalized'].unique().tolist())
    # Display the selected option
    st.write("You selected:", selected_option_theater)


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

    selected_option_intelligence = st.selectbox("Select an option for Intelligence Level(Preference order(0-1)) :", df['intelligence_normalized'].unique().tolist())
    # Display the selected option
    st.write("You selected:", selected_option_intelligence)

    selected_option_sincere = st.selectbox("Select an option for Sincere Level(Preference order(0-1)) :", df['sincere_normalized'].unique().tolist())
    # Display the selected option
    st.write("You selected:", selected_option_sincere)

  

with col3:
    
    selected_option_ambition = st.selectbox("Select an option for Ambition Level(Preference order(0-1)) :", df['ambition_normalized'].unique().tolist())
    # Display the selected option
    st.write("You selected:", selected_option_ambition)

    selected_option_funny = st.selectbox("Select an option for Funny Personality Level(Preference order(0-1)) :", df['funny_normalized'].unique().tolist())
    # Display the selected option
    st.write("You selected:", selected_option_funny)

    selected_option_attractive = st.selectbox("Select an option for Attractive Personality Level(Preference order(0-1)) :", df['attractive_normalized'].unique().tolist())
    # Display the selected option
    st.write("You selected:", selected_option_attractive)
    
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

  



user_preferences = {'age': int(selected_option_age),
                'gender': selected_option_gender,
                'race': selected_option_race,
                'field': selected_option_field,
                'yoga_normalized':selected_option_yoga,
                'shopping_normalized':selected_option_shopping,
                'concerts_normalized':selected_option_concert,
                'theater_normalized':selected_option_theater,
                'reading_normalized':selected_option_reading,
                'gaming_normalized':selected_option_gaming,
                'art_normalized':selected_option_art,
                'music_normalized':selected_option_music,
                'dining_normalized':selected_option_dining,
                'movies_normalized':selected_option_movie,
                'tv_normalized':selected_option_tv,
                'clubbing_normalized':selected_option_clubbing,
                'hiking_normalized':selected_option_hiking,
                'museums_normalized':selected_option_meseums,
                'exercise_normalized':selected_option_exercise,
                'sports_normalized':selected_option_sports,
                'intelligence_normalized':selected_option_intelligence,
                'sincere_normalized':selected_option_sincere,
                'ambition_normalized':selected_option_ambition,
                'funny_normalized':selected_option_funny,
                'attractive_normalized':selected_option_attractive,
            }

interested_records = []
for index , row in df.iterrows():
    # logging.info(f'Iterating row number {index}')
    for key,value in user_preferences.items():
        if row[key]== user_preferences[key]:
            
            df.loc[index,'compatbilityScore'] +=1
            interested_records.append(index)
            
            
# interestedDf =  df.iloc[interested_records][['age','gender','race','field','yoga_normalized','shopping_normalized','concerts_normalized','compatbilityScore']]


compatible_df = df[df['compatbilityScore'] != 0][['age','gender','race','field','yoga_normalized','shopping_normalized','concerts_normalized','compatbilityScore']]
compatible_sorted_df = compatible_df.sort_values(by='compatbilityScore', ascending=False)
st.title("Interested Records - Sorted by Compatibility Score")
styled_sorted_df = compatible_sorted_df.style.set_properties(**{'background-color': 'white', 'color': 'black'})
st.dataframe(styled_sorted_df)


# # Combine the interested records into a DataFrame
# interested_df = pd.DataFrame(interested_records)

# Display the interested records table
# st.title("Interested Records")
# # st.dataframe(interestedDf)
# st.table(compatible_sorted_df)