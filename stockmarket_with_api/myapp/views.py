from rest_framework.response import Response
from rest_framework.views import APIView
import http.client
import json
import yfinance as yf
import pandas as pd
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta

class TopCompaniesAPIView(APIView):
    def get(self, request):
        top_100_companies = {
    "AAPL": "Apple Inc.",
    "MSFT": "Microsoft Corporation",
    "GOOGL": "Alphabet Inc. (Class A)",
    "GOOG": "Alphabet Inc. (Class C)",
    "AMZN": "Amazon.com Inc.",
    "TSLA": "Tesla Inc.",
    "NVDA": "NVIDIA Corporation",
    "BRK.B": "Berkshire Hathaway Inc. (Class B)",
    "META": "Meta Platforms Inc.",
    "V": "Visa Inc.",
    "UNH": "UnitedHealth Group Incorporated",
    "JNJ": "Johnson & Johnson",
    "XOM": "Exxon Mobil Corporation",
    "PG": "Procter & Gamble Company",
    "JPM": "JPMorgan Chase & Co.",
    "MA": "Mastercard Incorporated",
    "HD": "The Home Depot Inc.",
    "LLY": "Eli Lilly and Company",
    "PFE": "Pfizer Inc.",
    "ABBV": "AbbVie Inc.",
    "MRK": "Merck & Co., Inc.",
    "PEP": "PepsiCo Inc.",
    "KO": "The Coca-Cola Company",
    "CVX": "Chevron Corporation",
    "TMO": "Thermo Fisher Scientific Inc.",
    "MCD": "McDonald's Corporation",
    "COST": "Costco Wholesale Corporation",
    "AVGO": "Broadcom Inc.",
    "DIS": "The Walt Disney Company",
    "ADBE": "Adobe Inc.",
    "CSCO": "Cisco Systems Inc.",
    "NKE": "NIKE Inc.",
    "CMCSA": "Comcast Corporation",
    "ORCL": "Oracle Corporation",
    "VZ": "Verizon Communications Inc.",
    "NFLX": "Netflix Inc.",
    "ABT": "Abbott Laboratories",
    "INTC": "Intel Corporation",
    "WMT": "Walmart Inc.",
    "LIN": "Linde plc",
    "MDT": "Medtronic plc",
    "NEE": "NextEra Energy Inc.",
    "TMUS": "T-Mobile US Inc.",
    "HON": "Honeywell International Inc.",
    "TXN": "Texas Instruments Incorporated",
    "MS": "Morgan Stanley",
    "BAC": "Bank of America Corporation",
    "CRM": "Salesforce Inc.",
    "UNP": "Union Pacific Corporation",
    "AMGN": "Amgen Inc.",
    "SBUX": "Starbucks Corporation",
    "BA": "The Boeing Company",
    "RTX": "Raytheon Technologies Corporation",
    "BLK": "BlackRock Inc.",
    "IBM": "International Business Machines Corporation",
    "GS": "The Goldman Sachs Group Inc.",
    "CAT": "Caterpillar Inc.",
    "CVS": "CVS Health Corporation",
    "GE": "General Electric Company",
    "LMT": "Lockheed Martin Corporation",
    "PYPL": "PayPal Holdings Inc.",
    "QCOM": "QUALCOMM Incorporated",
    "DHR": "Danaher Corporation",
    "UPS": "United Parcel Service Inc.",
    "PM": "Philip Morris International Inc.",
    "AMAT": "Applied Materials Inc.",
    "C": "Citigroup Inc.",
    "LOW": "Lowe's Companies Inc.",
    "MU": "Micron Technology Inc.",
    "SPGI": "S&P Global Inc.",
    "INTU": "Intuit Inc.",
    "MDLZ": "Mondelez International Inc.",
    "PLD": "Prologis Inc.",
    "SCHW": "The Charles Schwab Corporation",
    "NOW": "ServiceNow Inc.",
    "ADI": "Analog Devices Inc.",
    "BMY": "Bristol-Myers Squibb Company",
    "MMM": "3M Company",
    "TGT": "Target Corporation",
    "BKNG": "Booking Holdings Inc.",
    "ISRG": "Intuitive Surgical Inc.",
    "EL": "The Estée Lauder Companies Inc.",
    "DE": "Deere & Company",
    "MO": "Altria Group Inc.",
    "GILD": "Gilead Sciences Inc.",
    "TJX": "The TJX Companies Inc.",
    "DUK": "Duke Energy Corporation",
    "FIS": "Fidelity National Information Services Inc.",
    "HUM": "Humana Inc.",
    "PGR": "The Progressive Corporation",
    "ADP": "Automatic Data Processing Inc.",
    "FDX": "FedEx Corporation",
    "COF": "Capital One Financial Corporation",
    "ZTS": "Zoetis Inc.",
    "SYK": "Stryker Corporation",
    "SO": "The Southern Company",
    "BSX": "Boston Scientific Corporation",
    "MMC": "Marsh & McLennan Companies Inc.",
    "BDX": "Becton, Dickinson and Company",
    "WM": "Waste Management Inc.",
    "SHW": "The Sherwin-Williams Company",
    "LRCX": "Lam Research Corporation",
    "CL": "Colgate-Palmolive Company",
    "PXD": "Pioneer Natural Resources Company"
    }
        return Response({"companies": top_100_companies})



class CurrentPriceAPIView(APIView):
    def get(self, request, ticker):
        conn = http.client.HTTPSConnection("yahoo-finance15.p.rapidapi.com")

        headers = {
            'x-rapidapi-key': "8a4a5012f9msh121486b60fb4e3cp1dd9afjsnafde66c0eca8",
            'x-rapidapi-host': "yahoo-finance15.p.rapidapi.com"
        }
        var=ticker

        conn.request("GET", f"/api/v1/markets/quote?ticker={var}&type=STOCKS", headers=headers)
        res = conn.getresponse()
        data = res.read()

        json_data = json.loads(data.decode("utf-8"))
        try:
            value = json_data['body']['primaryData']['lastSalePrice']
            net_change = json_data['body']['primaryData']['netChange']
            percentage_change = json_data['body']['primaryData']['percentageChange']
            timee = json_data['body']['primaryData']['lastTradeTimestamp']
        except KeyError as e:
            return Response({"error": f"Error extracting data: {e}"}, status=400)

        return Response({
            'ticker': ticker,
            'value': value,
            'net_change': net_change,
            'percentage_change': percentage_change,
            'time': timee
        })


class PriceHistoryAPIView(APIView):
    def get(self, request, ticker):
        ticker_obj = yf.Ticker(ticker)
        history_data = ticker_obj.history(period="max")

        if history_data.empty:
            return Response({"error": "Historical data not available"}, status=404)

        history_data.index = pd.to_datetime(history_data.index)
        history_data = history_data.loc["1990-01-01":].copy()

        history_data["Tomorrow"] = history_data["Close"].shift(-1)
        history_data = history_data.dropna()

        predictors = ["Close", "Volume", "Open", "High", "Low"]
        target = "Tomorrow"

        model = LinearRegression()
        model.fit(history_data[predictors], history_data[target])

        last_known_date = history_data.index[-1]
        future_dates = pd.date_range(last_known_date, periods=365, freq='B')[1:]

        future_data = pd.DataFrame(index=future_dates, columns=predictors)
        last_row = history_data.iloc[-1]

        for date in future_dates:
            future_data.loc[date] = last_row[predictors]
            predicted_close = model.predict([future_data.loc[date]])[0]
            future_data.loc[date, "Close"] = predicted_close
            last_row = future_data.loc[date]

        try:
            tomorrow_date = datetime.now() + timedelta(days=3)
            datee = tomorrow_date.strftime("%Y-%m-%d")
            predicted_close_25_aug = str(future_data.loc[datee]["Close"])[:6]
        except KeyError:
            return Response({"error": f"Holiday on {datee}, so no data available"}, status=404)

        return Response({
            'ticker': ticker,
            'predicted_close': predicted_close_25_aug,
            'date': datee
        })

