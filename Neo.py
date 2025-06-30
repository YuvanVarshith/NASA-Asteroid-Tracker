import requests
import pprint
from datetime import datetime
import mysql.connector

#Establishing connection with API
link= "https://api.nasa.gov/neo/rest/v1/feed?start_date=2024-01-01&end_date=2024-01-07&api_key=qfYTxRudMLefkOsVgRORdjjRfacFWoXvlwcDoTeh"
response = requests.get(link)
data = response.json()

#Extracting Data Using NASA's Asteroid API

asteriodes_data= [] 
target = 200
while len(asteriodes_data) < target:
  response = requests.get(link)
  data = response.json()
  details = data['near_earth_objects']
  for date, asteriodes in details.items():
    for ast in asteriodes:
      asteriodes_data.append(dict(id=int(ast['id']),
                                 neo_reference_id=ast['neo_reference_id'],
                                 name=ast['name'],
                                 absolute_magnitude_h=ast['absolute_magnitude_h'],
                                 estimated_diameter_min_km=ast['estimated_diameter']['kilometers']['estimated_diameter_min'],
                                 estimated_diameter_max_km=ast['estimated_diameter']['kilometers']['estimated_diameter_max'],
                                 is_potentially_hazardous_asteroid=ast['is_potentially_hazardous_asteroid'],
                                 close_approach_date=datetime.strptime(ast['close_approach_data'][0]["close_approach_date"], '%Y-%m-%d').date(),
                                 relative_velocity_kmph=float(ast['close_approach_data'][0]["relative_velocity"]['kilometers_per_hour']),
                                 astronomical=float(ast['close_approach_data'][0]['miss_distance']['astronomical']),
                                 miss_distance_km=float(ast['close_approach_data'][0]['miss_distance']['kilometers']),
                                 miss_distance_lunar=float(ast['close_approach_data'][0]['miss_distance']['lunar']),
                                 orbiting_body=ast['close_approach_data'][0]['orbiting_body']))
      if len(asteriodes_data) >= target:
        break
    if len(asteriodes_data) >= target:
      break
  url = data['links']['next']

#Databse connection
connection = mysql.connector.connect(host='gateway01.ap-southeast-1.prod.aws.tidbcloud.com',
                               user='3AgaX31voqjKoCg.root',
                               password='B0VUhselpkYfTPPK',
                               port = 4000)

cursor = connection.cursor()
cursor.execute("create database dummy")

#selecting database
cursor.execute("USE dummy")

#Creating Asteroids table
cursor.execute("""CREATE TABLE asteroids(id INT, name VARCHAR(200), absolute_magnitude_h FLOAT, estimated_diameter_min_km FLOAT, estimated_diameter_max_km FLOAT, is_potentially_hazardous_asteroid BOOLEAN)""")

#Creating Close Approach Table
cursor.execute("""CREATE TABLE close_approach(neo_reference_id INT, close_approach_date DATE, relative_velocity_kmph FLOAT, astronomical FLOAT, miss_distance_km FLOAT, miss_distance_lunar FLOAT, orbiting_body VARCHAR(400))""")

#Inserting into Asteroids tables
for asteroid in asteriodes_data:
  cursor.execute("""
  INSERT INTO asteroids (
    id,
    name, 
    absolute_magnitude_h, 
    estimated_diameter_min_km, 
    estimated_diameter_max_km, 
    is_potentially_hazardous_asteroid
  ) VALUES (%s, %s, %s, %s, %s, %s)""", (
      asteroid["id"],
      asteroid["name"],
      asteroid["absolute_magnitude_h"],
      asteroid["estimated_diameter_min_km"],
      asteroid["estimated_diameter_max_km"],
      asteroid["is_potentially_hazardous_asteroid"]
  ))

# Inserting into Close Approach tables
for asteroid in asteriodes_data:
  cursor.execute("""
  INSERT INTO close_approach (
    neo_reference_id,
    close_approach_date, 
    relative_velocity_kmph, 
    astronomical, 
    miss_distance_km, 
    miss_distance_lunar,
    orbiting_body
  ) VALUES (%s, %s, %s, %s, %s, %s, %s)""", (
      asteroid["neo_reference_id"],
      asteroid["close_approach_date"],
      asteroid["relative_velocity_kmph"],
      asteroid["astronomical"],
      asteroid["miss_distance_km"],
      asteroid["miss_distance_lunar"],
      asteroid["orbiting_body"]
  ))