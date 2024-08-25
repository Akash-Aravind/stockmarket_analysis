import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
import numpy as np

df = pd.read_csv(r"D:\Programming\mytechathon\stockmarket_techathon\stock_data.csv")

df.dropna(inplace=True)

features = ['Open', 'High', 'Low', 'Close', 'Volume']
X = df[features]
y = df['Close'] 

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='mean')), 
    ('regressor', LinearRegression())
])

pipeline.fit(X_train, y_train)

linear_y_pred = pipeline.predict(X_test)

average_prediction = np.mean(linear_y_pred)

print(f"Average Predicted Close Price for Test Set = {average_prediction:.2f}")
print("Linear Regression MSE:", mean_squared_error(y_test, linear_y_pred))
