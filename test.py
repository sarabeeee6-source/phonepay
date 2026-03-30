# %%
#!git clone https://github.com/PhonePe/pulse.git

# %%
import os
path="D:/Sara/New folder/Saravana/Phonepay/pulse/data/aggregated/user/country/india/state"
Agg_state_list=os.listdir(path)
Agg_state_list

# %%
#Once created the clone of GIT-HUB repository then,
#Required libraries for the program

import pandas as pd
import json
import os

#This is to direct the path to get the data as states

path="D:/Sara/New folder/Saravana/Phonepay/pulse/data/aggregated/transaction/country/india/state"
Agg_state_list=os.listdir(path)
#Agg_state_list--> to get the list of states in India

#<------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------>#

#This is to extract the data's to create a dataframe

clm={'State':[], 'Year':[],'Quarter':[],'Transaction_type':[], 'Transaction_count':[], 'Transaction_amount':[]}

for i in Agg_state_list:
    p_i=os.path.join(path,i)
    Agg_yr=os.listdir(p_i)
    for j in Agg_yr:
        p_j=os.path.join(p_i,j)
        Agg_yr_list=os.listdir(p_j)
        for k in Agg_yr_list:
            p_k=os.path.join(p_j,k)
            Data=open(p_k,'r')
            D=json.load(Data)
            for z in D['data']['transactionData']:
              Name=z['name']
              count=z['paymentInstruments'][0]['count']
              amount=z['paymentInstruments'][0]['amount']
              clm['Transaction_type'].append(Name)
              clm['Transaction_count'].append(count)
              clm['Transaction_amount'].append(amount)
              clm['State'].append(i)
              clm['Year'].append(j)
              clm['Quarter'].append(int(k.strip('.json')))
#Succesfully created a dataframe
Agg_Trans=pd.DataFrame(clm)
Agg_Trans.to_csv("agg_transaction.csv", index=False)


# %%
import os
import json
import pandas as pd

# Base path to aggregated user device data
path = r"D:/Sara/New folder/Saravana/Phonepay/pulse/data/aggregated/user/country/india/state"

clm = {
    'State': [], 
    'Year': [], 
    'Quarter': [], 
    'Brand': [], 
    'Count': [], 
    'Percentage': []
}

# Loop through states
for state in os.listdir(path):
    state_path = os.path.join(path, state)
    if not os.path.isdir(state_path):
        continue

    # Loop through years
    for year in os.listdir(state_path):
        year_path = os.path.join(state_path, year)
        if not os.path.isdir(year_path):
            continue

        # Loop through quarters
        for quarter in os.listdir(year_path):
            quarter_path = os.path.join(year_path, quarter)
            if not os.path.isfile(quarter_path):
                continue

            # Open JSON file
            with open(quarter_path, 'r') as f:
                D = json.load(f)

                # ✅ Users by device
                users = D.get('data', {}).get('usersByDevice')
                if users:
                    for z in users:
                        clm['State'].append(state)
                        clm['Year'].append(year)
                        clm['Quarter'].append(int(quarter.strip('.json')))
                        clm['Brand'].append(z['brand'])
                        clm['Count'].append(z['count'])
                        clm['Percentage'].append(z['percentage'])

# Convert to DataFrame
Agg_user = pd.DataFrame(clm)

# Save to CSV
Agg_user.to_csv("agg_user.csv", index=False)


# %%
import pandas as pd
import json
import os

#This is to direct the path to get the data as states

path="D:/Sara/New folder/Saravana/Phonepay/pulse/data/aggregated/insurance/country/india/state"
Agg_state_list=os.listdir(path)
#Agg_state_list--> to get the list of states in India

#<------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------>#

#This is to extract the data's to create a dataframe

clm={'State':[], 'Year':[],'Quarter':[],'Insurance_type':[], 'Insurance_count':[], 'Insurance_amount':[]}

for i in Agg_state_list:
    p_i=os.path.join(path,i)
    Agg_yr=os.listdir(p_i)
    for j in Agg_yr:
        p_j=os.path.join(p_i,j)
        Agg_yr_list=os.listdir(p_j)
        for k in Agg_yr_list:
            p_k=os.path.join(p_j,k)
            Data=open(p_k,'r')
            D=json.load(Data)
            for z in D['data']['transactionData']:
              Name=z['name']
              count=z['paymentInstruments'][0]['count']
              amount=z['paymentInstruments'][0]['amount']
              clm['Insurance_type'].append(Name)
              clm['Insurance_count'].append(count)
              clm['Insurance_amount'].append(amount)
              clm['State'].append(i)
              clm['Year'].append(j)
              clm['Quarter'].append(int(k.strip('.json')))
#Succesfully created a dataframe
Agg_Insurance=pd.DataFrame(clm)
Agg_Insurance.to_csv("agg_insurance.csv", index=False)


# %%
#Once created the clone of GIT-HUB repository then,
#Required libraries for the program

import pandas as pd
import json
import os

#This is to direct the path to get the data as states

path="D:/Sara/New folder/Saravana/Phonepay/pulse/data/map/transaction/hover/country/india/state"
Agg_state_list=os.listdir(path)
#Agg_state_list--> to get the list of states in India

#<------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------>#

#This is to extract the data's to create a dataframe

clm={'State':[], 'Year':[],'Quarter':[],'Transaction_type':[], 'Transaction_count':[], 'Transaction_amount':[]}

for i in Agg_state_list:
    p_i=os.path.join(path,i)
    Agg_yr=os.listdir(p_i)
    for j in Agg_yr:
        p_j=os.path.join(p_i,j)
        Agg_yr_list=os.listdir(p_j)
        for k in Agg_yr_list:
            p_k=os.path.join(p_j,k)
            Data=open(p_k,'r')
            D=json.load(Data)
            for z in D['data']['hoverDataList']:
              Name=z['name']
              count=z['metric'][0]['count']
              amount=z['metric'][0]['amount']
              clm['Transaction_type'].append(Name)
              clm['Transaction_count'].append(count)
              clm['Transaction_amount'].append(amount)
              clm['State'].append(i)
              clm['Year'].append(j)
              clm['Quarter'].append(int(k.strip('.json')))
#Succesfully created a dataframe
map_Trans=pd.DataFrame(clm)
map_Trans.to_csv("map_transaction.csv", index=False)


# %%
#Once created the clone of GIT-HUB repository then,
#Required libraries for the program

import pandas as pd
import json
import os

#This is to direct the path to get the data as states

path="D:/Sara/New folder/Saravana/Phonepay/pulse/data/map/user/hover/country/india/state"
Agg_state_list=os.listdir(path)
#Agg_state_list--> to get the list of states in India

#<------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------>#

import os
import json
import pandas as pd

# Base path to aggregated user district-level data
path = r"D:/Sara/New folder/Saravana/Phonepay/pulse/data/map/user/hover/country/india/state"

clm = {
    'State': [], 
    'Year': [], 
    'Quarter': [], 
    'District': [], 
    'RegisteredUsers': [], 
    'AppOpens': []
}

# Loop through states
for state in os.listdir(path):
    state_path = os.path.join(path, state)
    if not os.path.isdir(state_path):
        continue

    # Loop through years
    for year in os.listdir(state_path):
        year_path = os.path.join(state_path, year)
        if not os.path.isdir(year_path):
            continue

        # Loop through quarters
        for quarter in os.listdir(year_path):
            quarter_path = os.path.join(year_path, quarter)
            if not os.path.isfile(quarter_path):
                continue

            # Open JSON file
            with open(quarter_path, 'r') as f:
                D = json.load(f)

                # Safely get hoverData
                hover_data = D.get('data', {}).get('hoverData')
                if hover_data:
                    for district, values in hover_data.items():
                        clm['State'].append(state)
                        clm['Year'].append(year)
                        clm['Quarter'].append(int(quarter.strip('.json')))
                        clm['District'].append(district)
                        clm['RegisteredUsers'].append(values.get('registeredUsers', 0))
                        clm['AppOpens'].append(values.get('appOpens', 0))
                else:
                    print(f"No hoverData in {quarter_path}")

# Convert to DataFrame
map_user = pd.DataFrame(clm)

map_user.to_csv("map_user.csv", index=False)


# %%
#Once created the clone of GIT-HUB repository then,
#Required libraries for the program

import pandas as pd
import json
import os

#This is to direct the path to get the data as states

path="D:/Sara/New folder/Saravana/Phonepay/pulse/data/map/insurance/hover/country/india/state"
Agg_state_list=os.listdir(path)
#Agg_state_list--> to get the list of states in India

#<------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------>#

#This is to extract the data's to create a dataframe

clm={'State':[], 'Year':[],'Quarter':[],'District':[], 'Total_count':[], 'Total_amount':[]}

for i in Agg_state_list:
    p_i=os.path.join(path,i)
    Agg_yr=os.listdir(p_i)
    for j in Agg_yr:
        p_j=os.path.join(p_i,j)
        Agg_yr_list=os.listdir(p_j)
        for k in Agg_yr_list:
            p_k=os.path.join(p_j,k)
            Data=open(p_k,'r')
            D=json.load(Data)
            for z in D['data']['hoverDataList']:
              District=z['name']
              count=z['metric'][0]['count']
              amount=z['metric'][0]['amount']
              clm['District'].append(District)
              clm['Total_count'].append(count)
              clm['Total_amount'].append(amount)
              clm['State'].append(i)
              clm['Year'].append(j)
              clm['Quarter'].append(int(k.strip('.json')))
#Succesfully created a dataframe
map_Insurance=pd.DataFrame(clm)
map_Insurance.to_csv("map_insurance.csv", index=False)


# %%
#Once created the clone of GIT-HUB repository then,
#Required libraries for the program

import pandas as pd
import json
import os

#This is to direct the path to get the data as states

path="D:/Sara/New folder/Saravana/Phonepay/pulse/data/top/transaction/country/india/state"
Agg_state_list=os.listdir(path)
#Agg_state_list--> to get the list of states in India

#<------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------>#

#This is to extract the data's to create a dataframe

import os
import json
import pandas as pd

# Base path to aggregated map transaction data
path = r"D:/Sara/New folder/Saravana/Phonepay/pulse/data/top/transaction/country/india/state"

clm = {
    'State': [], 
    'Year': [], 
    'Quarter': [], 
    'Level': [],        # "district" or "pincode"
    'EntityName': [], 
    'Count': [], 
    'Amount': []
}

# Loop through states
for state in os.listdir(path):
    state_path = os.path.join(path, state)
    if not os.path.isdir(state_path):
        continue

    # Loop through years
    for year in os.listdir(state_path):
        year_path = os.path.join(state_path, year)
        if not os.path.isdir(year_path):
            continue

        # Loop through quarters
        for quarter in os.listdir(year_path):
            quarter_path = os.path.join(year_path, quarter)
            if not os.path.isfile(quarter_path):
                continue

            # Open JSON file
            with open(quarter_path, 'r') as f:
                D = json.load(f)

                # ✅ Districts
                districts = D.get('data', {}).get('districts')
                if districts:
                    for z in districts:
                        clm['State'].append(state)
                        clm['Year'].append(year)
                        clm['Quarter'].append(int(quarter.strip('.json')))
                        clm['Level'].append("district")
                        clm['EntityName'].append(z['entityName'])
                        clm['Count'].append(z['metric']['count'])
                        clm['Amount'].append(z['metric']['amount'])

                # ✅ Pincodes
                pincodes = D.get('data', {}).get('pincodes')
                if pincodes:
                    for z in pincodes:
                        clm['State'].append(state)
                        clm['Year'].append(year)
                        clm['Quarter'].append(int(quarter.strip('.json')))
                        clm['Level'].append("pincode")
                        clm['EntityName'].append(z['entityName'])
                        clm['Count'].append(z['metric']['count'])
                        clm['Amount'].append(z['metric']['amount'])

# Convert to DataFrame
Top_Trans = pd.DataFrame(clm)
Top_Trans = Top_Trans.fillna(0)
Top_Trans.to_csv("top_transaction.csv", index=False)


# %%
import os
import json
import pandas as pd

# Base path to top user data
path = r"D:/Sara/New folder/Saravana/Phonepay/pulse/data/top/user/country/india/state"

clm = {
    'State': [], 
    'Year': [], 
    'Quarter': [], 
    'Level': [],        # "district" or "pincode"
    'EntityName': [], 
    'RegisteredUsers': []
}

# Loop through states
for state in os.listdir(path):
    state_path = os.path.join(path, state)
    if not os.path.isdir(state_path):
        continue

    # Loop through years
    for year in os.listdir(state_path):
        year_path = os.path.join(state_path, year)
        if not os.path.isdir(year_path):
            continue

        # Loop through quarters
        for quarter in os.listdir(year_path):
            quarter_path = os.path.join(year_path, quarter)
            if not os.path.isfile(quarter_path):
                continue

            # Open JSON file
            with open(quarter_path, 'r') as f:
                D = json.load(f)

                # ✅ Districts
                districts = D.get('data', {}).get('districts')
                if districts:
                    for z in districts:
                        clm['State'].append(state)
                        clm['Year'].append(year)
                        clm['Quarter'].append(int(quarter.strip('.json')))
                        clm['Level'].append("district")
                        clm['EntityName'].append(z['name'])
                        clm['RegisteredUsers'].append(z['registeredUsers'])

                # ✅ Pincodes
                pincodes = D.get('data', {}).get('pincodes')
                if pincodes:
                    for z in pincodes:
                        clm['State'].append(state)
                        clm['Year'].append(year)
                        clm['Quarter'].append(int(quarter.strip('.json')))
                        clm['Level'].append("pincode")
                        clm['EntityName'].append(z['name'])
                        clm['RegisteredUsers'].append(z['registeredUsers'])

# Convert to DataFrame
top_user = pd.DataFrame(clm)
top_user.to_csv("top_user.csv", index=False)


# %%
import os
import json
import pandas as pd

# Base path to top transaction  data
path = r"D:/Sara/New folder/Saravana/Phonepay/pulse/data/top/insurance/country/india/state"

clm = {
    'State': [], 
    'Year': [], 
    'Quarter': [], 
    'Level': [],        # "district" or "pincode"
    'EntityName': [], 
    'Count': [], 
    'Amount': []
}

# Loop through states
for state in os.listdir(path):
    state_path = os.path.join(path, state)
    if not os.path.isdir(state_path):
        continue

    # Loop through years
    for year in os.listdir(state_path):
        year_path = os.path.join(state_path, year)
        if not os.path.isdir(year_path):
            continue

        # Loop through quarters
        for quarter in os.listdir(year_path):
            quarter_path = os.path.join(year_path, quarter)
            if not os.path.isfile(quarter_path):
                continue

            # Open JSON file
            with open(quarter_path, 'r') as f:
                D = json.load(f)

                # ✅ Districts
                districts = D.get('data', {}).get('districts')
                if districts:
                    for z in districts:
                        clm['State'].append(state)
                        clm['Year'].append(year)
                        clm['Quarter'].append(int(quarter.strip('.json')))
                        clm['Level'].append("district")
                        clm['EntityName'].append(z['entityName'])
                        clm['Count'].append(z['metric']['count'])
                        clm['Amount'].append(z['metric']['amount'])

                # ✅ Pincodes
                pincodes = D.get('data', {}).get('pincodes')
                if pincodes:
                    for z in pincodes:
                        clm['State'].append(state)
                        clm['Year'].append(year)
                        clm['Quarter'].append(int(quarter.strip('.json')))
                        clm['Level'].append("pincode")
                        clm['EntityName'].append(z['entityName'])
                        clm['Count'].append(z['metric']['count'])
                        clm['Amount'].append(z['metric']['amount'])

# Convert to DataFrame
top_insurance = pd.DataFrame(clm)
top_insurance=top_insurance.fillna(0)
top_insurance.to_csv("top_insurance.csv", index=False)


# %%
import pymysql

# Connect to MySQL
conn = pymysql.connect(
    host="localhost",
    user="root",
    password="root",
    database="phonepay"
)

# --- Create table ---
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS agg_transaction (
    State VARCHAR(100),
    Year INT,
    Quarter INT,
    Transaction_type VARCHAR(50),
    Transaction_count BIGINT,
    Transaction_amount DECIMAL(18,2)
)
""")
conn.commit()
cursor.close()

# --- Insert data ---
cursor = conn.cursor()

for _, row in Agg_Trans.iterrows():
    cursor.execute("""
        INSERT INTO agg_transaction (State, Year, Quarter, Transaction_type, Transaction_count, Transaction_amount)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        row['State'],
        row['Year'],
        row['Quarter'],
        row['Transaction_type'],
        row['Transaction_count'],
        row['Transaction_amount']
    ))

conn.commit()
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS agg_user (
    State VARCHAR(100),
    Year INT,
    Quarter INT,
    Brand VARCHAR(50),
    Count BIGINT,
    Percentage DECIMAL(10,6)
)
""")
for _, row in Agg_user.iterrows():
    cursor.execute("""
        INSERT INTO Agg_user (State, Year, Quarter, Brand, Count, Percentage)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        row['State'],
        row['Year'],
        row['Quarter'],
        row['Brand'],
        row['Count'],
        row['Percentage']
    ))  

conn.commit()
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS agg_insurance (
    State VARCHAR(100),
    Year INT,
    Quarter INT,
    Insurance_type VARCHAR(50),
    Insurance_count BIGINT,
    Insurance_amount DECIMAL(18,2)
)
""");
for _, row in Agg_Insurance.iterrows():
    cursor.execute("""
        INSERT INTO agg_insurance (State, Year, Quarter, Insurance_type, Insurance_count, Insurance_amount)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        row['State'],
        row['Year'],
        row['Quarter'],
        row['Insurance_type'],
        row['Insurance_count'],
        row['Insurance_amount']
    ))  

conn.commit()
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS map_transaction (
    State VARCHAR(100),
    Year INT,
    Quarter INT,
    Transaction_type VARCHAR(50),
    Transaction_count BIGINT,
    Transaction_amount DECIMAL(18,2)
)
""");
for _, row in map_Trans.iterrows():
    cursor.execute("""
        INSERT INTO map_transaction (State, Year, Quarter, Transaction_type, Transaction_count, Transaction_amount)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        row['State'],
        row['Year'],
        row['Quarter'],
        row['Transaction_type'],
        row['Transaction_count'],
        row['Transaction_amount']
    ))  
conn.commit()   
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS map_user (
    State VARCHAR(100),
    Year INT,
    Quarter INT,
    District VARCHAR(100),
    RegisteredUsers BIGINT,
    AppOpens BIGINT
)
""");
for _, row in map_user.iterrows():
    cursor.execute("""
        INSERT INTO map_user (State, Year, Quarter, District, RegisteredUsers, AppOpens)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        row['State'],
        row['Year'],
        row['Quarter'],
        row['District'],
        row['RegisteredUsers'],
        row['AppOpens']
    ))      
conn.commit()
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS map_insurance (
    State VARCHAR(100),
    Year INT,
    Quarter INT,
    District VARCHAR(100),
    Total_count BIGINT,
    Total_amount DECIMAL(18,2)
)
""");
for _, row in map_Insurance.iterrows():
    cursor.execute("""
        INSERT INTO map_insurance (State, Year, Quarter, District, Total_count, Total_amount)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        row['State'],
        row['Year'],
        row['Quarter'],
        row['District'],
        row['Total_count'],
        row['Total_amount']
    ))      
conn.commit()       
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS top_transaction (
    State VARCHAR(100),
    Year INT,
    Quarter INT,
    Level VARCHAR(50),
    EntityName VARCHAR(100),
    Count BIGINT,
    Amount DECIMAL(18,2)
)
""");
for _, row in Top_Trans.iterrows():
    cursor.execute("""
        INSERT INTO top_transaction (State, Year, Quarter, Level, EntityName, Count, Amount)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        row['State'],
        row['Year'],
        row['Quarter'],
        row['Level'],
        row['EntityName'],
        row['Count'],
        row['Amount']
    ))
conn.commit()
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS top_user (
    State VARCHAR(100),
    Year INT,
    Quarter INT,
    Level VARCHAR(50),
    EntityName VARCHAR(100),
    RegisteredUsers BIGINT
)
""");
for _, row in top_user.iterrows():
    cursor.execute("""
        INSERT INTO top_user (State, Year, Quarter, Level, EntityName, RegisteredUsers)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        row['State'],
        row['Year'],
        row['Quarter'],
        row['Level'],
        row['EntityName'],
        row['RegisteredUsers']
    ))
conn.commit()
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS top_insurance (
    State VARCHAR(100),
    Year INT,
    Quarter INT,
    Level VARCHAR(50),
    EntityName VARCHAR(100),
    Count BIGINT,
    Amount DECIMAL(18,2)
)
""");
for _, row in top_insurance.iterrows():
    cursor.execute("""
        INSERT INTO top_insurance (State, Year, Quarter, Level, EntityName, Count, Amount)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        row['State'],
        row['Year'],
        row['Quarter'],
        row['Level'],
        row['EntityName'],
        row['Count'],
        row['Amount']
    ))
conn.commit()



cursor.close()
conn.close()

# %%
import streamlit as st
import pandas as pd
import sqlalchemy
import plotly.express as px

# -----------------------------
# Database connection settings
# -----------------------------
# Example for MySQL; change URL for PostgreSQL, SQL Server, etc.
DB_URL = "mysql+pymysql://root:root@localhost:3306/phonepay"

# Create SQLAlchemy engine
try:
    engine = sqlalchemy.create_engine(DB_URL)
except Exception as e:
    st.error(f"Database connection failed: {e}")
    st.stop()

# -----------------------------
# Fetch data from SQL
# -----------------------------
import pymysql

# Connect to MySQL
conn = pymysql.connect(
    host="localhost",
    user="root",
    password="root",
    database="phonepay"
)

# --- Create table ---
cursor = conn.cursor()
cursor.execute( """
SELECT 
    State,
    Year,
    SUM(Transaction_count) AS total_transaction_count,
    SUM(Transaction_amount) AS total_transaction_amount
FROM agg_transaction
GROUP BY State, Year
ORDER BY Year;
""")

results = cursor.fetchall()
cursor.close()
conn.close()

# -----------------------------
# Build DataFrame
# -----------------------------
df = pd.DataFrame(
    results,
    columns=['State', 'Year', 'total_transaction_count', 'total_transaction_amount']
)

# -----------------------------
# Load GeoJSON for India states
# -----------------------------
# Make sure you have india_states.geojson file in your project folder
with open("india_states.geojson", "r") as f:
    india_states = json.load(f)

# -----------------------------
# Streamlit UI
# -----------------------------
st.title("PhonePe Pulse 2D Map")

# Dropdown to choose metric
metric = st.selectbox(
    "Select Metric to Display:",
    ["total_transaction_count", "total_transaction_amount"]
)

# -----------------------------
# Plot Choropleth Map
# -----------------------------
fig = px.choropleth(
    df,
    geojson=india_states,
    locations="State",
    featureidkey="properties.ST_NM",  # adjust based on your geojson file
    color=metric,
    hover_name="State",
    animation_frame="Year",           # animate by year
    title=f"Year-wise {metric.replace('_',' ').title()} across States"
)

fig.update_geos(fitbounds="locations", visible=False)

st.plotly_chart(fig, width="stretch")