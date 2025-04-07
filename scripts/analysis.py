import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load cleaned data
file_path = "D:/air_quality_project/data/cleaned_dataset.csv"
data = pd.read_csv(file_path, parse_dates=["Date"])

# Plot pollution trends over time
plt.figure(figsize=(10, 5))
pollutants = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']
for pollutant in pollutants:
    plt.plot(data['Date'], data[pollutant], label=pollutant)
plt.title("Pollution Trends Over Time")
plt.legend()
plt.savefig("D:/air_quality_project/data/trends.png")
plt.show()

# Correlation matrix
plt.figure(figsize=(8, 6))
sns.heatmap(data.corr(), annot=True, cmap="coolwarm")
plt.title("Correlation Matrix")
plt.savefig("D:/air_quality_project/data/correlation_matrix.png")
plt.show()
