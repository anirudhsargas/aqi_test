# Air Quality Analysis Project

## Project Structure
- **data/**: Contains the raw dataset and cleaned dataset.
- **scripts/**:
  - preprocess.py: Preprocesses the raw dataset.
  - analysis.py: Analyzes and visualizes trends and correlations.
  - modeling.py: Builds predictive models for pollutants.
- **dashboard/**:
  - index.html: Interactive dashboard for visualizations.
  - styles.css: Styling for the dashboard.
  - app.js: Dynamic visualizations using Chart.js.

## How to Run
1. Preprocess data: `python scripts/preprocess.py`
2. Analyze data: `python scripts/analysis.py`
3. Train and evaluate models: `python scripts/modeling.py`
4. View dashboard: Open `dashboard/index.html` in a browser.

data/
  raw_dataset.csv
  cleaned_data.csv
  correlations.csv
scripts/
  preprocess.py
  analysis.py 
  modeling.py
dashboard/
  index.html
  styles.css
  app.js
app.py
requirements.txt
README.md


Core Packages:
- numpy==1.26.4
- pandas==2.2.1
- scipy==1.13.0
- statsmodels==0.14.1
- pmdarima==2.0.4
- scikit-learn==1.4.0
- flask==3.0.2
- werkzeug==3.0.1

Supporting Packages:
- patsy==0.5.6
- python-dateutil==2.9.0
- pytz==2025.1