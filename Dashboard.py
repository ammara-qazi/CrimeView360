import streamlit as st
import pandas as pd
import seaborn as sns
from sqlalchemy import create_engine
import os
import matplotlib.pyplot as plt

# Set up the SQLAlchemy connection
db_username = os.getenv('Db_USER')
db_password = os.getenv('Db_PASSWORD')
engine = create_engine(f'mysql+mysqlconnector://{db_username}:{db_password}@localhost/crimeview360(1)')

# Dashboard Title
st.title("CrimeView360 Dashboard")

# KPIs (Summary Metrics)
st.header("Key Metrics")
col1, col2 = st.columns(2)
col1.metric("Total Incidents", "2520")
col2.metric("Open Cases", "1300", "-2%")

# Top Row Layout
# Top Row Layout
st.header("Crime Insights")
main_col1, main_col2 = st.columns([2, 1])  # Adjust proportions for larger and smaller columns

    # Top 10 Locations (Bar Chart)
query = "SELECT location FROM location"
data = pd.read_sql(query, engine)

top_locations = data['location'].value_counts().head(10)
fig1, ax1 = plt.subplots(figsize=(8, 6))  # Adjust size
colors = sns.color_palette("pastel", len(top_locations))
top_locations.plot(kind='barh', color=colors, ax=ax1)
ax1.set_title("Top 10 Locations", fontsize=16, fontweight='bold')  # Removed title
ax1.set_xlabel("Number of Incidents", fontsize=15)
ax1.set_ylabel("Locations", fontsize=15)
ax1.grid(axis='x', linestyle='--', alpha=0.7)
st.pyplot(fig1)

# Left Column: Incident Categories and Top 10 Locations
with main_col1:
    # Incident Categories (Pie Chart)
    query3 = "SELECT id,type FROM crime"
    data3 = pd.read_sql(query3, engine)

    if 'Type' in data3.columns:
        incident_categories = data3['Type'].value_counts()
    elif 'type' in data3.columns:
        incident_categories = data3['type'].value_counts()

    fig3, ax3 = plt.subplots(figsize=(8, 6))  # Larger figure size
    incident_categories.head(10).plot(
        kind='pie',
        autopct='%1.1f%%',
        startangle=90,
        colors=plt.cm.Set3.colors,
        textprops={'fontsize': 10},
        ax=ax3
    )
    ax3.set_title("Incident Categories", fontsize=16, fontweight='bold')  # Removed title
    ax3.set_ylabel("")
    st.pyplot(fig3)



# Right Column: Count of Arrests and Day-wise Crime Rates
with main_col2:
    # Count of Arrests
    query2 = "SELECT * FROM incident"
    data2 = pd.read_sql(query2, engine)

    arrest_counts = data2['Arrest'].value_counts()
    fig2, ax2 = plt.subplots(figsize=(6, 4))  # Adjust size
    arrest_counts.plot(kind='bar', color=['skyblue', 'salmon'], ax=ax2)
    ax2.set_title("Number Of Arrest", fontsize=14, fontweight='bold')
    ax2.set_xlabel("Arrest Status", fontsize=12)
    ax2.set_ylabel("Count", fontsize=12)
    ax2.set_xticks([0, 1])
    ax2.set_xticklabels(['Wanted', 'Arrested'], rotation=0)
    st.pyplot(fig2)

    # Day-wise Crime Rates
    query4 = "SELECT Date FROM incident"
    data4 = pd.read_sql(query4, engine)

    if 'Date' in data4.columns:
        data4['Date'] = pd.to_datetime(data4['Date'])
        may_data = data4[data4['Date'].dt.month == 5]
        daywise_crime = may_data.groupby(may_data['Date'].dt.day).size()
    elif 'date' in data4.columns:
        data4['date'] = pd.to_datetime(data4['date'])
        may_data = data4[data4['date'].dt.month == 5]
        daywise_crime = may_data.groupby(may_data['date'].dt.day).size()

    fig4, ax4 = plt.subplots(figsize=(6, 5))  # Adjust size
    ax4.plot(daywise_crime.index, daywise_crime.values, marker='o', color='green')
    ax4.set_title("Day-wise Crime Rates", fontsize=14, fontweight='bold') 
    ax4.set_xlabel("Day of the Month", fontsize=12)
    ax4.set_ylabel("Number of Crimes", fontsize=12)
    ax4.grid(True, linestyle='--', alpha=0.7)
    st.pyplot(fig4)

# Dispose of the engine connection
engine.dispose()
