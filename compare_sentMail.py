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
import os
from datetime import datetime
import pandas as pd

import os
from datetime import datetime
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Directory where your files are located
directory = "data"
# Email configuration
smtp_server = "your_smtp_server.com"
smtp_port = 587
smtp_username = "your_email@example.com"
smtp_password = "your_email_password"
sender_email = "your_email@example.com"
recipient_email = "recipient_email@example.com"

def get_timestamp(filename):
    try:
        timestamp_str = filename.split("_rawdata")[0]
        timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d_%H-%M-%S")
        return timestamp
    except ValueError:
        return None

def send_email(subject, message):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        print("Email sent successfully.")
    except Exception as e:
        print(f"Email sending failed: {str(e)}")

# List all files in the directory
files = os.listdir(directory)
valid_files = [file for file in files if get_timestamp(file) is not None]

# Sort the valid files based on timestamps in descending order
valid_files.sort(key=lambda x: get_timestamp(x), reverse=True)

# Ensure at least two valid files exist
if len(valid_files) < 2:
    print("Not enough valid files found.")
else:
    # Get the filenames of the two most recent files
    most_recent_file = valid_files[0]
    second_most_recent_file = valid_files[1]

    most_recent_file_path = os.path.join(directory, most_recent_file)
    second_most_recent_file_path = os.path.join(directory, second_most_recent_file)

    # Read data from the most recent and second most recent files (assuming they're CSV)
    most_recent_df = pd.read_csv(most_recent_file_path)
    second_most_recent_df = pd.read_csv(second_most_recent_file_path)

    # Compare the two DataFrames
    if not most_recent_df.equals(second_most_recent_df):
        # If there are changes, send an email with the notification
        print("lol")
        # send_email("Data Update", "The data has been updated.")




df = pd.DataFrame(data, columns=["From", "To", "Inclusions", "Earliest Pick up", "Latest Drop off", "Vehicle type", "Rate", "Days allowed", "Extra days"])
df = df.dropna()
filtered_df = df[df["Vehicle type"].str.contains("2 Person|van", case=False, na=False) | 
                 df["From"].str.contains("San Francisco", case=False, na=False) |
                 df["To"].str.contains("San Francisco", case=False, na=False)]