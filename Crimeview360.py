from sqlalchemy import create_engine
import pandas as pd
import matplotlib.pyplot as plt
import os
from colorama import Fore, Style
import seaborn as sns

db_username = os.getenv('Db_USER')
db_password = os.getenv('Db_PASSWORD')
# SQLAlchemy connection string
engine = create_engine(f'mysql+mysqlconnector://{db_username}:{db_password}@localhost/crimeview360(1)')

#heading
print(Fore.BLUE + Style.BRIGHT + "\n\n=== Welcome to CrimeView360 ===" + Style.RESET_ALL)


# SQL Query 1:TOP 10 CRIME LOCATION

print(Fore.GREEN + Style.BRIGHT + "\nTOP 10 LOCATIONS" + Style.RESET_ALL)
query = "SELECT location FROM location"
data = pd.read_sql(query, engine)
query5 = "SELECT location,count(location) FROM location group by location limit 10"
data5 = pd.read_sql(query5, engine)
# Check Data
print(data5.head(10))

colors = sns.color_palette("pastel", 10)

# Plot a bar chart
data['location'].value_counts().head(10).plot(kind='barh', color=colors)
plt.title("TOP 10 CRIME LOCATIONS", fontsize=16, fontweight='bold', fontfamily='Arial')  # Change font and style
plt.ylabel("Categories", fontsize=12, fontfamily='Arial')
plt.xlabel("Counts", fontsize=12, fontfamily='Arial')
plt.grid(axis='x', linestyle='--', alpha=0.7)  # Add a grid for better readability
plt.tight_layout()  # Adjust layout for better aesthetics
plt.show()


# SQL Query 2:Count the number of Arrest
print(Fore.GREEN + Style.BRIGHT + "\nARREST HISTORY" + Style.RESET_ALL)

query6 = "SELECT Arrest,count(arrest) as Number_OF_Arrest FROM incident group by arrest"
data6= pd.read_sql(query6, engine)
# Check Data
print(data6.head(10))  # Display only the first few rows for better readability

query2 = "SELECT * FROM incident"
data2 = pd.read_sql(query2, engine)

# Count the number of True and False values in the Arrest column
arrest_counts = data2['Arrest'].value_counts()

# Plot a bar chart for Arrest counts
arrest_counts.plot(kind='bar', color=['skyblue', 'salmon'], edgecolor='black')
plt.title("Count of Arrests")
plt.xlabel("Arrest Status")
plt.ylabel("Count")
plt.xticks(ticks=[0, 1], labels=['Wanted', 'Arrested'], rotation=0)
plt.tight_layout()  # Adjust layout to prevent clipping
plt.show()


# SQL Query 3:Incident Categories
print(Fore.GREEN + Style.BRIGHT + "\nINCIDENT CATEGORIES" + Style.RESET_ALL)

query3 = "SELECT id,type FROM crime"
data3 = pd.read_sql(query3, engine)
query4="Select type,count(type) as Count from crime group by type"
data4 = pd.read_sql(query4, engine)

# Check Data
print(data4.head())  

# Ensure the correct column name for incident categories
if 'Type' in data3.columns:
    incident_categories = data3['Type'].value_counts()  # Assuming 'Type' is the column for incident categories
elif 'type' in data3.columns:
    incident_categories = data3['type'].value_counts()  # If column name is lowercase
else:
    raise KeyError("Column for incident categories not found. Please check the column names in the database.")

# Plot a pie chart for the most frequent categories
colors = plt.cm.Set3.colors  # Use a different color palette
incident_categories.head(10).plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=colors, textprops={'fontsize': 8})
plt.title("Top 10 Most Frequent Incident Categories", fontsize=12)
plt.ylabel("")  # Hide the y-axis label for better aesthetics
plt.tight_layout()
plt.show()

# SQL Query 4:Day-wise Crime Counts in May

query = "SELECT * FROM incident"
data = pd.read_sql(query, engine)

# Ensure the correct column for dates
if 'Date' in data.columns:
    data['Date'] = pd.to_datetime(data['Date'])  # Convert 'Date' column to datetime
elif 'date' in data.columns:
    data['date'] = pd.to_datetime(data['date'])  # If column is lowercase
else:
    raise KeyError("Column for dates not found. Please check the column names in the database.")

# Filter data for the 5th month (May)
if 'Date' in data.columns:
    may_data = data[data['Date'].dt.month == 5]
elif 'date' in data.columns:
    may_data = data[data['date'].dt.month == 5]

# Group by day and count occurrences
if 'Date' in data.columns:
    daywise_crime = may_data.groupby(may_data['Date'].dt.day).size()
elif 'date' in data.columns:
    daywise_crime = may_data.groupby(may_data['date'].dt.day).size()

# Plot the line graph for day-wise trend in May
plt.figure(figsize=(10, 6))
plt.plot(daywise_crime.index, daywise_crime.values, marker='o', color='green', label='Crime Rate')
plt.title("Day-wise Crime Rates in May", fontsize=14)
plt.xlabel("Day of the Month", fontsize=12)
plt.ylabel("Number of Crimes", fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.xticks(daywise_crime.index)  # Show each day on the x-axis
plt.legend()
plt.tight_layout()
plt.show()

print(Fore.GREEN + Style.BRIGHT + "\nDay-wise Crime Counts in May" + Style.RESET_ALL)
print(daywise_crime)

# Dispose of the engine connection (optional)
engine.dispose()

