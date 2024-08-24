
import yfinance as yf
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Fetch historical data
ticker = yf.Ticker("MSFT")
sp500 = ticker.history(period="max")

# Preprocess the data
sp500.index = pd.to_datetime(sp500.index)
sp500 = sp500.loc["1990-01-01":].copy()

# Shift 'Close' to create 'Tomorrow' and remove irrelevant columns
sp500["Tomorrow"] = sp500["Close"].shift(-1)
sp500 = sp500.dropna()

# Define the features (predictors) and target
predictors = ["Close", "Volume", "Open", "High", "Low"]
target = "Tomorrow"

# Split the data into train and test sets
train = sp500.iloc[:-1]  # All data except the last one for training
test = sp500.iloc[-1:]   # The last row for testing/prediction

# Train the Linear Regression model
model = LinearRegression()
model.fit(train[predictors], train[target])

# Predict the closing price for tomorrow
predicted_close = model.predict(test[predictors])

# Print the actual prediction for tomorrow
print(f"Predicted Closing Price for Tomorrow: ${predicted_close[0]:.2f}")

# Evaluate the model on the previous 100 days
mse = mean_squared_error(train[target], model.predict(train[predictors]))
r2 = r2_score(train[target], model.predict(train[predictors]))

print(f"Mean Squared Error: {mse}")
print(f"R-squared: {r2}")

# Display actual vs predicted values for the test set
test['Predicted Close'] = predicted_close
print(test[['Tomorrow', 'Predicted Close']])

# Save the predictions to a CSV file if needed
test[['Tomorrow', 'Predicted Close']].to_csv('predicted_close_prices.csv')
