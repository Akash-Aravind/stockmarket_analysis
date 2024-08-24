import http.client
import json
import csv

# Establish connection
conn = http.client.HTTPSConnection("yahoo-finance15.p.rapidapi.com")

# Set headers
headers = {
    'x-rapidapi-key': "8a4a5012f9msh121486b60fb4e3cp1dd9afjsnafde66c0eca8",
    'x-rapidapi-host': "yahoo-finance15.p.rapidapi.com"
}

# Specify the stock symbol
var = "AAPL"

# Make the API request
conn.request("GET", f"/api/v1/markets/stock/history?symbol={var}&interval=5m&diffandsplits=false", headers=headers)
res = conn.getresponse()
data = res.read()

# Decode and parse the JSON data
json_data = json.loads(data.decode("utf-8"))

# Access the 'body' section
body = json_data.get('body', {})

# Define the CSV file name
csv_file = f"stock_data.csv"

# Open the CSV file for writing
with open(csv_file, 'w', newline='') as file:
    # Define the CSV writer
    writer = csv.writer(file)
    
    # Write the header
    writer.writerow(["Timestamp", "Date", "Date UTC", "Open", "High", "Low", "Close", "Volume"])
    
    # Loop through the 'body' section
    for timestamp, details in body.items():
        date = details.get('date', 'N/A')
        date_utc = details.get('date_utc', 'N/A')
        open_value = details.get('open', 'N/A')
        high = details.get('high', 'N/A')
        low = details.get('low', 'N/A')
        close = details.get('close', 'N/A')
        volume = details.get('volume', 'N/A')
        
        # Write the data to the CSV file
        writer.writerow([timestamp, date, date_utc, open_value, high, low, close, volume])

print(f"Data successfully written to {csv_file}")
