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


url = "https://www.transfercarus.com/search?sort_col=days&view_by=list&page=1"  # Replace with the actual URL

from bs4 import BeautifulSoup
import pandas as pd


soup = BeautifulSoup(url, 'html.parser')

# Initialize lists to store data
vehicle_titles = []
start_dates = []
end_dates = []
locations = []
free_days = []
extra_days = []
prices = []
available = []

# Find all vehicle listings
vehicle_listings = soup.find_all(class_='tile-shadowed')

# Loop through each listing and extract data
for listing in vehicle_listings:
    # Extract vehicle title
    vehicle_title = listing.find(class_='vehicle-title').text.strip()
    vehicle_titles.append(vehicle_title)

    # Extract start and end dates
    date_elements = listing.select('.route-description > .row > .col-lg-3')
    start_date = date_elements[0].text.strip()
    end_date = date_elements[1].text.strip()
    start_dates.append(start_date)
    end_dates.append(end_date)

    # Extract locations
    location_elements = listing.select('.route-locations > div')
    start_location = location_elements[0].text.strip()
    end_location = location_elements[1].text.strip()
    locations.append(f'{start_location} - {end_location}')

    # Extract free days
    free_days_element = listing.find(class_='nb-days').text.strip()
    free_days.append(free_days_element)

    # Extract extra days and prices
    extra_days_element = listing.find(class_='paid-days').text.strip()
    extra_days.append(extra_days_element)

    # Extract available information
    available_element = listing.find(class_='badge-warning').text.strip()
    available.append(available_element)

# Create a DataFrame
data = {
    'Vehicle Title': vehicle_titles,
    'Start Date': start_dates,
    'End Date': end_dates,
    'Locations': locations,
    'Free Days': free_days,
    'Extra Days': extra_days,
    'Available': available,
}

df = pd.DataFrame(data)

# Display the DataFrame
print(df)


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
