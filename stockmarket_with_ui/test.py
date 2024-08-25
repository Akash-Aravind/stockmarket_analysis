import http.client
import json

# Establish a connection to the Yahoo Finance API
conn = http.client.HTTPSConnection("yahoo-finance15.p.rapidapi.com")

# Define the headers with the API key and host
headers = {
    'x-rapidapi-key': "8a4a5012f9msh121486b60fb4e3cp1dd9afjsnafde66c0eca8",
    'x-rapidapi-host': "yahoo-finance15.p.rapidapi.com"
}

def fetch_page(page_number):
    conn.request("GET", f"/api/v2/markets/tickers?page={page_number}&type=STOCKS", headers=headers)
    res = conn.getresponse()
    data = res.read().decode("utf-8")
    return json.loads(data)

def main():
    total_pages = 3  # Limit to the first 5 pages
    all_tickers = []

    for current_page in range(1, total_pages + 1):
        print(f"\nFetching page {current_page}...")
        response = fetch_page(current_page)

        if 'body' in response:
            tickers = response['body']
            if not tickers:
                print(f"No tickers available on page {current_page}.")
                break

            all_tickers.extend(tickers)
        else:
            print(f"Error fetching data on page {current_page}.")
            break

    # Display all tickers from the first 5 pages
    print("\nAll Tickers from the first 5 pages:")
    for ticker in all_tickers:
        print(f"{ticker['symbol']} - {ticker['name']}")

main()
