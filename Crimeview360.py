from sqlalchemy import create_engine
import pandas as pd
import matplotlib.pyplot as plt
import os

db_username = os.getenv('Db_USER')
db_password = os.getenv('Db_PASSWORD')


# SQLAlchemy connection string
engine = create_engine(f'mysql+mysqlconnector://{db_username}:{db_password}@localhost/crimeview360(1)')

# SQL Query to Fetch Data
query = "SELECT * FROM location"
data = pd.read_sql(query, engine)

# Check Data
print(data)

# Plot a bar chart
data['location'].value_counts().head(10).plot(kind='bar',color=['indigo','violet'])
plt.title("TOP 10 CRIME LOCATION")
plt.xlabel("Categories")
plt.ylabel("Counts")
plt.show()

query2 = "SELECT * FROM incident"
data2 = pd.read_sql(query2, engine)

# Check Data
print(data2.head())  # Display only the first few rows for better readability

# Count the number of True and False values in the Arrest column
arrest_counts = data2['Arrest'].value_counts()

# Plot a bar chart for Arrest counts
arrest_counts.plot(kind='bar', color=['skyblue', 'salmon'], edgecolor='black')
plt.title("Count of Arrests (True vs False)")
plt.xlabel("Arrest Status")
plt.ylabel("Count")
plt.xticks(ticks=[0, 1], labels=['False', 'True'], rotation=0)
plt.tight_layout()  # Adjust layout to prevent clipping
plt.show()

# SQL Query to Fetch Data
query3 = "SELECT * FROM crime"
data3 = pd.read_sql(query3, engine)

# Check Data
print(data3.head())  # Display only the first few rows for better readability

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

# Dispose of the engine connection (optional)
engine.dispose()

