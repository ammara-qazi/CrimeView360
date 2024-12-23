import streamlit as st
from sqlalchemy import create_engine
import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt

# SQLAlchemy connection string
db_username = os.getenv('Db_USER')
db_password = os.getenv('Db_PASSWORD')
engine = create_engine(f'mysql+mysqlconnector://{db_username}:{db_password}@localhost/crimeview360(1)')

# Streamlit setup
st.set_page_config(page_title="CrimeView360 Dashboard", layout="wide")

# Heading
st.title("CrimeView360 Dashboard")

# Section 1: Top 10 Crime Locations
st.header("Top 10 Crime Locations")
query5 = "SELECT location, count(location) as Count FROM location GROUP BY location ORDER BY Count DESC LIMIT 10"
data5 = pd.read_sql(query5, engine)

# Display data as a table
st.write(data5)

# Bar chart
fig, ax = plt.subplots()
sns.barplot(data=data5, x="Count", y="location", palette="pastel", ax=ax)
ax.set_title("Top 10 Crime Locations", fontsize=16, fontweight='bold')
ax.set_xlabel("Count")
ax.set_ylabel("Location")
st.pyplot(fig)

# Section 2: Arrest History
st.header("Arrest History")
query6 = "SELECT Arrest, count(Arrest) as Number_OF_Arrest FROM incident GROUP BY Arrest"
data6 = pd.read_sql(query6, engine)
st.write(data6)

# Arrest bar chart
query2 = "SELECT Arrest FROM incident"
data2 = pd.read_sql(query2, engine)
arrest_counts = data2['Arrest'].value_counts()

fig, ax = plt.subplots()
arrest_counts.plot(kind='bar', color=['skyblue', 'salmon'], edgecolor='black', ax=ax)
ax.set_title("Count of Arrests")
ax.set_xlabel("Arrest Status")
ax.set_ylabel("Count")
ax.set_xticks([0, 1])
ax.set_xticklabels(['Wanted', 'Arrested'])
st.pyplot(fig)

# Section 3: Incident Categories
st.header("Incident Categories")
query4 = "SELECT type, count(type) as Count FROM crime GROUP BY type"
data4 = pd.read_sql(query4, engine)
st.write(data4)

# Incident categories pie chart
incident_categories = data4.set_index('type')['Count']
fig, ax = plt.subplots()
incident_categories.plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=plt.cm.Set3.colors, textprops={'fontsize': 8}, ax=ax)
ax.set_title("Top Incident Categories")
ax.set_ylabel("")
st.pyplot(fig)

# Section 4: Day-wise Crime Counts in May
st.header("Day-wise Crime Counts in May")
query = "SELECT Date FROM incident"
data = pd.read_sql(query, engine)

# Ensure the correct column for dates
data['Date'] = pd.to_datetime(data['Date'])
may_data = data[data['Date'].dt.month == 5]
daywise_crime = may_data.groupby(may_data['Date'].dt.day).size()

# Line chart
fig, ax = plt.subplots()
ax.plot(daywise_crime.index, daywise_crime.values, marker='o', color='green', label='Crime Rate')
ax.set_title("Day-wise Crime Rates in May", fontsize=14)
ax.set_xlabel("Day of the Month", fontsize=12)
ax.set_ylabel("Number of Crimes", fontsize=12)
ax.grid(True, linestyle='--', alpha=0.7)
ax.legend()
st.pyplot(fig)

# Display data
st.write(daywise_crime)

# Dispose of the engine connection
engine.dispose()
