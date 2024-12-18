from sqlalchemy import create_engine
import pandas as pd

# SQLAlchemy connection string
engine = create_engine('mysql+mysqlconnector://root:rabia765@localhost/crimeview360(1)')

# SQL Query to Fetch Data
query = "SELECT * FROM location"
data = pd.read_sql(query, engine)

# Check Data
print(data)

import matplotlib.pyplot as plt

# Plot a bar chart
data['location'].value_counts().head(10).plot(kind='bar')
plt.title("Location Chart Example")
plt.xlabel("Categories")
plt.ylabel("Counts")
plt.show()

# Dispose of the engine connection (optional)
engine.dispose()