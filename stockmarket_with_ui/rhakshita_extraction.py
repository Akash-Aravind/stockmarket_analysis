import http.client
import json
import csv

conn = http.client.HTTPSConnection("yahoo-finance15.p.rapidapi.com")

headers = {
    'x-rapidapi-key': "8a4a5012f9msh121486b60fb4e3cp1dd9afjsnafde66c0eca8",
    'x-rapidapi-host': "yahoo-finance15.p.rapidapi.com"
}

var = "AAPL"

conn.request("GET", f"/api/v1/markets/stock/history?symbol={var}&interval=5m&diffandsplits=false", headers=headers)
res = conn.getresponse()
data = res.read()

json_data = json.loads(data.decode("utf-8"))

body = json_data.get('body', {})

csv_file = f"stock_data.csv"

with open(csv_file, 'w', newline='') as file:
    writer = csv.writer(file)
    
    writer.writerow(["Timestamp", "Date", "Date UTC", "Open", "High", "Low", "Close", "Volume"])
    
    for timestamp, details in body.items():
        date = details.get('date', 'N/A')
        date_utc = details.get('date_utc', 'N/A')
        open_value = details.get('open', 'N/A')
        high = details.get('high', 'N/A')
        low = details.get('low', 'N/A')
        close = details.get('close', 'N/A')
        volume = details.get('volume', 'N/A')
        
        writer.writerow([timestamp, date, date_utc, open_value, high, low, close, volume])

print(f"Data successfully written to {csv_file}")
