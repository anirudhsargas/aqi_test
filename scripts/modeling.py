import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# Load cleaned data
file_path = "D:/air_quality_project/data/cleaned_dataset.csv"
data = pd.read_csv(file_path)

# Define features and target
X = data[['PM10', 'SO2', 'NO2', 'CO', 'O3']]
y = data['PM2.5']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = LinearRegression()
model.fit(X_train, y_train)

# Evaluate model
predictions = model.predict(X_test)
mse = mean_squared_error(y_test, predictions)
print(f"Mean Squared Error: {mse}")
