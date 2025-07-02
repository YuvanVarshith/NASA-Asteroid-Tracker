import mysql.connector
import pandas as pd
import streamlit as st
from datetime import date

# SQL database connection setup
conn = mysql.connector.connect(host='gateway01.ap-southeast-1.prod.aws.tidbcloud.com',
                               user='3AgaX31voqjKoCg.root',
                               password='B0VUhselpkYfTPPK',
                               database="dummy",
                               port = 4000)

#query to fetch data
query = """
SELECT a.absolute_magnitude_h,a.estimated_diameter_min_km,a.estimated_diameter_max_km,ca.relative_velocity_kmph,ca.astronomical,a.is_potentially_hazardous_asteroid,ca.close_approach_date
FROM close_approach ca
JOIN asteroids a ON ca.neo_reference_id = a.id
"""
# Using cursor 
cursor = conn.cursor()
cursor.execute(query)
rows = cursor.fetchall()
columns = [desc[0] for desc in cursor.description]
df = pd.DataFrame(rows, columns=columns)
cursor.close()

#Streamlit app page design
if "active_page" not in st.session_state:
    st.session_state.active_page = "home"

# sidebar buttons design 
with st.sidebar:
    st.markdown("### 📡 Asteroid Approaches")
    if st.button("🔴 Filter Criteria"):
        st.session_state.active_page = "filter"
    if st.button("🗃️ Queries"):
        st.session_state.active_page = "queries"

# title
st.markdown("<h1 style='text-align: center;'>🚀 NASA Asteroid Tracker 🌠</h1>", unsafe_allow_html=True)

# Page: Filter Criteria
if st.session_state.active_page == "filter":
    col1, col2, col3 = st.columns(3)

    with col1:
        min_mag = st.slider("Min Magnitude", float(df['absolute_magnitude_h'].min()),
                            float(df['absolute_magnitude_h'].max()),
                            float(df['absolute_magnitude_h'].min()))
        min_dia = st.slider("Min Estimated Diameter (km)", float(df['estimated_diameter_min_km'].min()),
                            float(df['estimated_diameter_min_km'].max()),
                            float(df['estimated_diameter_min_km'].min()))
        max_dia = st.slider("Max Estimated Diameter (km)", 0.0,
                            float(df['estimated_diameter_max_km'].max()),
                            float(df['estimated_diameter_max_km'].max()))

    with col2:
        vel_range = st.slider("Relative_velocity_kmph Range",
                              float(df['relative_velocity_kmph'].min()),
                              float(df['relative_velocity_kmph'].max()),
                              (float(df['relative_velocity_kmph'].min()),
                               float(df['relative_velocity_kmph'].max())))
        au = st.slider("Astronomical unit",
                       float(df["astronomical"].min()),
                       float(df["astronomical"].max()),
                       float(df["astronomical"].min()))
        hazardous = st.selectbox("Only Show Potentially Hazardous", ["0", "1"])

    with col3:
        start_date = st.date_input("Start Date", date(2024, 1, 1))
        end_date = st.date_input("End Date", date(2025, 4, 13))

    # Filtering
    filtered_df = df[
        (df["absolute_magnitude_h"] >= min_mag) &
        (df["estimated_diameter_min_km"] >= min_dia) &
        (df["estimated_diameter_max_km"] <= max_dia) &
        (df["relative_velocity_kmph"] >= vel_range[0]) &
        (df["relative_velocity_kmph"] <= vel_range[1]) &
        (df["astronomical"] >= au) &
        (df["is_potentially_hazardous_asteroid"] == int(hazardous)) &
        (pd.to_datetime(df["close_approach_date"]) >= pd.to_datetime(start_date)) &
        (pd.to_datetime(df["close_approach_date"]) <= pd.to_datetime(end_date))
    ]

    st.success(f"✅ Filter applied! {len(filtered_df)} asteroids matched your criteria.")
    st.markdown("### 📋 Filtered Asteroids")
    st.dataframe(filtered_df, use_container_width=True)

# Page: Queries
elif st.session_state.active_page == "queries":
    st.markdown("### 🗃️ Custom Queries")
     
    query_options = {
        "Count how many times each asteroid has approached Earth": """
            select name, count(*) as num_of_times_approached_earth from asteroids
            where is_potentially_hazardous_asteroid =1
            group by name;
        """,
        "Average velocity of each asteroid over multiple approaches": """
            select a.name, avg(ca.relative_velocity_kmph) as average_velocity from asteroids a
            join close_approach ca on ca.neo_reference_id = a.id
            group by a.name;
        """,
        "List top 10 fastest asteroids": """
            select a.name, max(ca.relative_velocity_kmph) as speed from asteroids a
            join close_approach ca on ca.neo_reference_id = a.id
            group by a.name
            order by speed desc
            limit 10;
        """,
        "Find potentially hazardous asteroids that have approached Earth more than 3 times": """
            select a.name, count(*) as approach_count from asteroids a
            join close_approach ca on a.id = ca.neo_reference_id
            where a.is_potentially_hazardous_asteroid = true
            group by a.name
            having count(*) > 3
            order by approach_count desc;
        """,
        "Find the month with the most asteroid approaches": """
            select month(close_approach_date) as approach_month, count(*) as total_approaches from close_approach 
            group by approach_month 
            order by total_approaches desc 
            limit 1;
        """,
        "Get the asteroid with the fastest ever approach speed":"""
            select a.name, ca.relative_velocity_kmph from asteroids a
            join close_approach ca on ca.neo_reference_id = a.id
            order by ca.relative_velocity_kmph limit 1;
        """,
        "Sort asteroids by maximum estimated diameter (descending)":"""
            select name, estimated_diameter_max_km from asteroids
            order by estimated_diameter_max_km desc;
        """,
        "Display the name of each asteroid along with the date and miss distance of its closest approach to Earth.":"""
            select a.name, ca.close_approach_date as close_date, ca.miss_distance_km from  asteroids a
            join close_approach ca on ca.neo_reference_id = a.id
            where orbiting_body = 'Earth';
        """,
        "List names of asteroids that approached Earth with velocity > 50,000 km/h":"""
            select a.name, ca.relative_velocity_kmph from  asteroids a
            join close_approach ca on ca.neo_reference_id = a.id
            where orbiting_body = 'Earth' and relative_velocity_kmph > 50000;
        """,
        "Count how many approaches happened per day":"""
            select day(close_approach_date),count(*) from close_approach
            group by day(close_approach_date)
            order by day(close_approach_date)
        """,
        "An asteroid whose closest approach is getting nearer over time":"""
            select a.name, ca.close_approach_date, ca.miss_distance_km from asteroids a
            join close_approach ca on ca.neo_reference_id = a.id
            order by a.name, ca.close_approach_date;
        """,
        "Find asteroid with the highest brightness (lower magnitude value)":"""
            select name, absolute_magnitude_h as lower_magnitude_value from asteroids 
            order by absolute_magnitude_h asc limit 1;
        """,
        "Get number of hazardous vs non-hazardous asteroids":"""
            select is_potentially_hazardous_asteroid, count(*) as total from asteroids
            group by is_potentially_hazardous_asteroid;
        """,
        "Find asteroids that passed closer than the Moon (lesser than 1 LD), along with their close approach date and distance":"""
            select a.name, ca.close_approach_date, ca.miss_distance_lunar from asteroids a
            join close_approach ca on ca.neo_reference_id = a.id
            where ca.miss_distance_lunar < 1
            order by ca.miss_distance_lunar;
        """,
        "Find asteroids that came within 0.05 AU(astronomical distance)":"""
            select a.name, ca.close_approach_date, ca.astronomical from asteroids a
            join close_approach ca on ca.neo_reference_id = a.id
            where ca.astronomical < 0.05
            order by ca.astronomical;
        """,
        "find the average size of all asteroids":"""
            select avg((estimated_diameter_min_km + estimated_diameter_max_km) / 2) as average_diameter_km from asteroids;
        """,
        "find the total number of unique asteroids":"""
            select count(distinct id) as unique_asteroid_count from asteroids;
        """,
        "Which asteroid has had the most close approaches to Earth":"""
            select a.name,  count(*) as approach_count  from  asteroids a 
            join close_approach ca  on  a.id = ca.neo_reference_id
            group by a.name
            order by approach_count desc limit 1;
        """,
        "find the earliest recorded close approach":"""
            select a.name, ca.close_approach_date from asteroids a 
            join close_approach ca on a.id = ca.neo_reference_id 
            order by ca.close_approach_date asc limit 1;
        """,
        "list asteroids that have approached earth more than once":"""
            select a.name, count(*) as approach_count from asteroids a 
            join close_approach ca on a.id = ca.neo_reference_id 
            group by a.name 
            having count(*) > 1 
            order by approach_count desc;
         """    
    }

    selected_query = st.selectbox("Select your query", ["Choose an option"] + list(query_options.keys()))

    if selected_query != "Choose an option":
        st.markdown(f"#### 🔍 Result for: **{selected_query}**")
        try:
            query_result_df = pd.read_sql(query_options[selected_query], conn)
            st.dataframe(query_result_df, use_container_width=True)
        except Exception as e:
            st.error(f"Error executing query: {e}")

# Page: Home 
else:
    st.markdown("👈 Click **Filter Criteria** or **Queries** from the sidebar to begin.")

# closing DB Connection
conn.close()