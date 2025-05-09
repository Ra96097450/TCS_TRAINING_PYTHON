import os
import logging
import pandas as pd
from flask import Flask, render_template, request
from pymongo import MongoClient
from statsmodels.tsa.statespace.sarimax import SARIMAX
from configparser import ConfigParser
from datetime import timedelta, datetime
import smtplib
from email.message import EmailMessage


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

def send_email(recipient_email, subject, body):
    sender_email = config.get('email', 'sender_email')
    sender_password = config.get('email', 'sender_password') #app password

    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = recipient_email

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.send_message(msg)
        logging.info(f"Forecast email sent to {recipient_email}")
        return True
    except Exception as e:
        logging.error(f"Failed to send email: {e}")
        return False

@app.route('/')
def index():
    start_time = datetime.now()
    logging.info(f"Starting weather forecast route {start_time}")
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
        start_date = ts.index[0]+ timedelta(days=1)
        date_list = [(start_date + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(10)]
        forecast_data = list(zip(date_list, predicted_temps))

        # Handle user input
        selected_date = request.args.get('selected_date')
        recipient_email = request.args.get('email')
        temp_for_selected_date = None
        message = None

        if selected_date:
            for date, temp in forecast_data:
                if date == selected_date:
                    temp_for_selected_date = temp
                    break

            # If email provided, send forecast
            if recipient_email and temp_for_selected_date is not None:
                subject = f"Weather Forecast for {selected_date}"
                body = f"The predicted temperature for Kolkata on {selected_date} is {temp_for_selected_date}°C."
                success = send_email(recipient_email, subject, body)
                message = "Email sent successfully!" if success else "Failed to send email."

        end_time = datetime.now()
        total_time = end_time - start_time

        logging.info(f"App ended at:{end_time}")
        logging.info(f"Total time taken by the App:{total_time}")

        return render_template("index.html",
                               forecast_data=forecast_data,
                               selected_date=selected_date,
                               temp_for_selected_date=temp_for_selected_date,
                               message=message)

    except Exception as e:
        logging.exception(f"Unhandled error: {e}")
        return "An error occurred during processing."

if __name__ == '__main__':
    app.run(debug=True)
