import pandas as pd

# Load dataset
file_path = "D:/air_quality_project/data/dataset.csv"

data = pd.read_csv(file_path, parse_dates=["Date"])

# Fill missing values
data.fillna(method='ffill', inplace=True)

# Extract useful features
data['Month'] = data['Date'].dt.month
data['Year'] = data['Date'].dt.year
# Save cleaned data
cleaned_file_path = "D:/air_quality_project/data/cleaned_dataset.csv"
data.to_csv(cleaned_file_path, index=False)
print("Preprocessing complete. Cleaned dataset saved.")
