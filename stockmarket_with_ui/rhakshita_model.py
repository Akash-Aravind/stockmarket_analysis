import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
import numpy as np

# Load data
df = pd.read_csv(r"D:\Programming\mytechathon\stockmarket_techathon\stock_data.csv")

# Drop rows with missing values (if any) or handle them
df.dropna(inplace=True)

# Define features and target variable
features = ['Open', 'High', 'Low', 'Close', 'Volume']
X = df[features]
y = df['Close']  # Target variable

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Impute missing values (if any) and define the pipeline
pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='mean')),  # Impute missing values with mean
    ('regressor', LinearRegression())
])

# Fit the pipeline on training data
pipeline.fit(X_train, y_train)

# Make predictions on the test set
linear_y_pred = pipeline.predict(X_test)

# Calculate summary statistics
average_prediction = np.mean(linear_y_pred)

# Print the average predicted value for the entire test set
print(f"Average Predicted Close Price for Test Set = {average_prediction:.2f}")

# Evaluate and print the performance of Linear Regression model
print("Linear Regression MSE:", mean_squared_error(y_test, linear_y_pred))
