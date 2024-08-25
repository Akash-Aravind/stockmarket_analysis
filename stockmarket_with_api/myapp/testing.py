import http.client
import json

conn = http.client.HTTPSConnection("yahoo-finance15.p.rapidapi.com")

headers = {
    'x-rapidapi-key': "8a4a5012f9msh121486b60fb4e3cp1dd9afjsnafde66c0eca8",
    'x-rapidapi-host': "yahoo-finance15.p.rapidapi.com"
}

tickers = ["AAPL", "GOOGL", "MSFT", "AMZN", "TSLA", "NFLX", "FB", "NVDA", "BABA", "INTC"]

print("Please select a ticker from the following list:")
for i, ticker in enumerate(tickers, 1):
    print(f"{i}. {ticker}")

selected_index = int(input("\nEnter the number corresponding to the ticker you want: ")) - 1

if 0 <= selected_index < len(tickers):
    selected_ticker = tickers[selected_index]

    conn.request("GET", f"/api/v1/markets/quote?ticker={selected_ticker}&type=STOCKS", headers=headers)

    res = conn.getresponse()
    data = res.read()

    json_data = json.loads(data.decode("utf-8"))

    try:
        print(json_data)
        last_sale_price = json_data['body']['primaryData']['lastSalePrice']
        print(f"Last sale price for {selected_ticker}: {last_sale_price}")
    except KeyError as e:
        print(f"Error extracting data: {e}")
else:
    print("Invalid selection. Please run the program again and select a valid number.")