import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import MinMaxScaler
from pmdarima import auto_arima
import warnings
warnings.filterwarnings('ignore')

# Configuration
DATA_PATH = 'data/air_quality.csv'
POLLUTANTS = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']
DATE_COL = 'Date'
START_DATE = '2020-01-01'
END_DATE = '2023-12-31'

def load_data():
    """Load and preprocess air quality data"""
    try:
        df = pd.read_csv(DATA_PATH, parse_dates=[DATE_COL])
        df = df[(df[DATE_COL] >= START_DATE) & (df[DATE_COL] <= END_DATE)]
        df.set_index(DATE_COL, inplace=True)
        
        # Handle missing values
        for pollutant in POLLUTANTS:
            df[pollutant] = df[pollutant].interpolate(method='time')
            
        return df
    
    except Exception as e:
        print(f"Error loading data: {str(e)}")
        return None

def analyze_pollutant(df, pollutant):
    """Perform complete analysis for one pollutant"""
    print(f"\n{'='*40}\nAnalyzing {pollutant}\n{'='*40}")
    
    # Time Series Decomposition
    decomposition = seasonal_decompose(df[pollutant], model='additive', period=24)
    decomposition.plot()
    plt.suptitle(f'{pollutant} Decomposition')
    plt.tight_layout()
    plt.show()
    
    # Stationarity Test
    print("\nStationarity Analysis:")
    adf_result = adfuller(df[pollutant])
    print(f'ADF Statistic: {adf_result[0]:.4f}')
    print(f'p-value: {adf_result[1]:.4f}')
    print('Critical Values:')
    for key, value in adf_result[4].items():
        print(f'   {key}: {value:.4f}')
    
    # ARIMA Modeling
    print("\nARIMA Modeling:")
    model = auto_arima(df[pollutant], seasonal=True, m=12,
                      suppress_warnings=True, stepwise=True)
    print(model.summary())
    
    # Forecast Visualization
    forecast = model.predict(n_periods=30)
    plt.figure(figsize=(12,6))
    plt.plot(df[pollutant], label='Historical')
    plt.plot(forecast, label='30-Day Forecast')
    plt.title(f'{pollutant} Forecast')
    plt.legend()
    plt.grid(True)
    plt.show()
    
    return model

def correlation_analysis(df):
    """Analyze correlations between pollutants"""
    print("\nCorrelation Analysis:")
    
    # Normalize data
    scaler = MinMaxScaler()
    normalized = pd.DataFrame(scaler.fit_transform(df[POLLUTANTS]), 
                            columns=POLLUTANTS, index=df.index)
    
    # Correlation Heatmap
    plt.figure(figsize=(10,8))
    sns.heatmap(normalized.corr(), annot=True, cmap='coolwarm', center=0)
    plt.title('Pollutant Correlation Matrix')
    plt.show()
    
    # Pairplot
    sns.pairplot(normalized.sample(100))
    plt.suptitle('Pollutant Relationships', y=1.02)
    plt.show()

def main():
    # Load and prepare data
    df = load_data()
    if df is None:
        return
    
    # Basic Info
    print("\nDataset Info:")
    print(df.info())
    print("\nDescriptive Statistics:")
    print(df[POLLUTANTS].describe())
    
    # Individual Pollutant Analysis
    models = {}
    for pollutant in POLLUTANTS:
        models[pollutant] = analyze_pollutant(df, pollutant)
    
    # Correlation Analysis
    correlation_analysis(df)
    
    # Save models
    print("\nSaving models...")
    for name, model in models.items():
        model.save(f'models/{name}_arima.pkl')

if __name__ == "__main__":
    main()