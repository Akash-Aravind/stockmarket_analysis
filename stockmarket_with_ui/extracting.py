
import yfinance as yf
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

ticker = yf.Ticker("MSFT")
sp500 = ticker.history(period="max")

sp500.index = pd.to_datetime(sp500.index)
sp500 = sp500.loc["1990-01-01":].copy()

sp500["Tomorrow"] = sp500["Close"].shift(-1)
sp500 = sp500.dropna()

predictors = ["Close", "Volume", "Open", "High", "Low"]
target = "Tomorrow"

train = sp500.iloc[:-1] 
test = sp500.iloc[-1:]   

model = LinearRegression()
model.fit(train[predictors], train[target])

predicted_close = model.predict(test[predictors])

print(f"Predicted Closing Price for Tomorrow: ${predicted_close[0]:.2f}")

mse = mean_squared_error(train[target], model.predict(train[predictors]))
r2 = r2_score(train[target], model.predict(train[predictors]))

print(f"Mean Squared Error: {mse}")
print(f"R-squared: {r2}")

test['Predicted Close'] = predicted_close
print(test[['Tomorrow', 'Predicted Close']])

test[['Tomorrow', 'Predicted Close']].to_csv('predicted_close_prices.csv')
