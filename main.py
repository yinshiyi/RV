import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import random
import time
import os
import seaborn as sns
from datetime import datetime, date, time, timezone
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


url = "https://imoova.com/imoova/relocations?region_id=3"  # Replace with the actual URL

# Send an HTTP request to the webpage and parse the HTML content
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

# Find the table element and extract the rows
table = soup.find("table", {"id": "dataTable"})
rows = table.find_all("tr")

# Initialize lists to store the data
data = []

for row in rows[1:]:  # Skip the header row
    cells = row.find_all("td")
    row_data = [cell.get_text(strip=True) for cell in cells[:9]]  # Keep only the first 11 values
    data.append(row_data)

# Create a Pandas DataFrame from the collected data and display it
df = pd.DataFrame(data, columns=["From", "To", "Inclusions", "Earliest Pick up", "Latest Drop off", "Vehicle type", "Rate", "Days allowed", "Extra days"])
df = df.dropna()
filtered_df = df[df["Vehicle type"].str.contains("2 Person|van", case=False, na=False) | 
                 df["From"].str.contains("San Francisco", case=False, na=False) |
                 df["To"].str.contains("San Francisco", case=False, na=False)]
# df = pd.DataFrame(data, columns=["From", "To", "Inclusions", "Earliest Pick up", "Latest Drop off", "Vehicle type", "Rate", "Days allowed", "Extra days"])
print(df)
#########################
today = datetime.now()
filename = os.path.join("data", f"{today.strftime('%Y-%m-%d_%H-%M-%S')}_rawdata.csv")
if not os.path.exists('data'):
    os.mkdir('data')
filtered_df.to_csv(filename, index=False)
