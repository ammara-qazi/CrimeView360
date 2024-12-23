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
st.write("A visual representation of crime data insights.")

# Create columns for layout
col1, col2 = st.columns(2)

# Section 1: Top 10 Crime Locations
with col1:
    query5 = "SELECT location, count(location) as Count FROM location GROUP BY location ORDER BY Count DESC LIMIT 10"
    data5 = pd.read_sql(query5, engine)

    # Bar chart
    fig, ax = plt.subplots()
    sns.barplot(data=data5, x="Count", y="location", hue="location", dodge=False, palette="pastel", ax=ax)
    ax.set_title("Top 10 Crime Locations", fontsize=12, fontweight='bold')
    ax.set_xlabel("Count")
    ax.set_ylabel("Location")
    ax.legend_.remove()  # Remove legend
    st.pyplot(fig)

# Section 2: Arrest History
with col2:
    query2 = "SELECT Arrest FROM incident"
    data2 = pd.read_sql(query2, engine)
    arrest_counts = data2['Arrest'].value_counts()

    # Arrest bar chart
    fig, ax = plt.subplots()
    arrest_counts.plot(kind='bar', color=['skyblue', 'salmon'], edgecolor='black', ax=ax)
    ax.set_title("Count of Arrests", fontsize=12, fontweight='bold')
    ax.set_xlabel("Arrest Status")
    ax.set_ylabel("Count")
    ax.set_xticks([0, 1])
    ax.set_xticklabels(['Wanted', 'Arrested'])
    st.pyplot(fig)

# Section 3: Incident Categories
with col1:
    query4 = "SELECT type, count(type) as Count FROM crime GROUP BY type"
    data4 = pd.read_sql(query4, engine)
    incident_categories = data4.set_index('type')['Count']

    # Pie chart
    fig, ax = plt.subplots()
    incident_categories.plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=plt.cm.Set3.colors, textprops={'fontsize': 8}, ax=ax)
    ax.set_title("Top Incident Categories", fontsize=12, fontweight='bold')
    ax.set_ylabel("")
    st.pyplot(fig)

# Section 4: Day-wise Crime Counts in May
with col2:
    query = "SELECT Date FROM incident"
    data = pd.read_sql(query, engine)
    data['Date'] = pd.to_datetime(data['Date'])
    may_data = data[data['Date'].dt.month == 5]
    daywise_crime = may_data.groupby(may_data['Date'].dt.day).size()

    # Line chart
    fig, ax = plt.subplots()
    ax.plot(daywise_crime.index, daywise_crime.values, marker='o', color='green', label='Crime Rate')
    ax.set_title("Day-wise Crime Rates in May", fontsize=12, fontweight='bold')
    ax.set_xlabel("Day of the Month")
    ax.set_ylabel("Number of Crimes")
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend()
    st.pyplot(fig)

# Dispose of the engine connection
engine.dispose()
