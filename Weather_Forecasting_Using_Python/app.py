
import os
import logging
import pandas as pd
from flask import Flask, render_template,request
from pymongo import MongoClient
from statsmodels.tsa.statespace.sarimax import SARIMAX
from configparser import ConfigParser
from datetime import timedelta

# Load configuration
config = ConfigParser()
config.read('config.ini')

# Logging setup
log_dir = config.get('logging', 'log_dir')
log_file = config.get('logging', 'log_file')
log_level = config.get('logging', 'log_level').upper()
log_mode = config.get('logging', 'log_file_mode')

os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(log_dir, log_file),
    filemode=log_mode,
    level=getattr(logging, log_level),
    format='%(asctime)s %(levelname)s [%(module)s:%(lineno)d] - %(message)s'
)

app = Flask(__name__)

@app.route('/')
def index():
    logging.info("Starting weather forecast route.")
    try:
        # MongoDB connection
        uri = config.get('mongodb', 'uri')
        db_name = config.get('mongodb', 'db')
        collection_name = config.get('mongodb', 'collection')
        client = MongoClient(uri)
        db = client[db_name]
        collection = db[collection_name]
        logging.info("Connected to MongoDB.")

        # Read data
        df = pd.DataFrame(list(collection.find()))
        df.columns = df.columns.str.strip()
        df['Date'] = pd.to_datetime(df['Date'])
        df.set_index('Date', inplace=True)
        df['Average Temperature (°C)'] = (df['Min Temperature (°C)'] + df['Max Temperature (°C)']) / 2
        logging.info("Data loaded and processed.")

        # Train model
        ts = df['Average Temperature (°C)']
        model = SARIMAX(ts, order=(1, 1, 1), seasonal_order=(1, 1, 1, 7),
                        enforce_stationarity=False, enforce_invertibility=False)
        results = model.fit(disp=False)
        logging.info("SARIMA model trained successfully.")

        # Forecast next 10 days
        forecast = results.get_forecast(steps=10)
        predicted_temps = forecast.predicted_mean.round(2)

        # Dates list
        start_date = ts.index[0] + timedelta(days=1)
        date_list = [(start_date + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(10)]

        logging.info("Next 10 days weather forecasting completed!")

        # Pair date and predicted temperature
        forecast_data = list(zip(date_list, predicted_temps))

        # Get selected date from user input
        selected_date = request.args.get('selected_date')
        temp_for_selected_date = None
        if selected_date:
            for date, temp in forecast_data:
                if date == selected_date:
                    temp_for_selected_date = temp
                    break

        return render_template("index.html", forecast_data=forecast_data, selected_date=selected_date,
                               temp_for_selected_date=temp_for_selected_date)
        



    except ValueError as ve:
        logging.error(f"ValueError: {ve}")
    except ConnectionError as ce:
        logging.error(f"ConnectionError: {ce}")
    except Exception as e:
        logging.exception(f"Unhandled error: {e}")

    return "An error occurred during processing."

if __name__ == '__main__':
    app.run(debug=True)
