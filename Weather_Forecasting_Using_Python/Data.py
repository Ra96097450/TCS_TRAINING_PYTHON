import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime, timedelta
import logging
import os
import configparser

# Load configuration
config = configparser.ConfigParser()
config.read('config.ini')

# Logging configuration
log_dir = config['logging']['log_dir']
log_file = config['logging']['log_file']
log_level = config['logging']['log_level'].upper()
log_file_mode = config['logging']['log_file_mode']

os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(log_dir, log_file),
    filemode=log_file_mode,
    level=getattr(logging, log_level),
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def fetch_weather_data():
    base_url = "https://www.timeanddate.com/weather/india/kolkata/historic"
    headers = {"User-Agent": "Mozilla/5.0"}

    csv_file_path = config['files']['csv_file']
    dates = [datetime.now() - timedelta(days=i) for i in range(1, 11)]
    formatted_dates = [date.strftime("%Y-%m-%d") for date in dates]
    weather_data = []

    for date_str in formatted_dates:
        try:
            params = {'hd': date_str.replace('-', '')}
            response = requests.get(base_url, headers=headers, params=params)
            response.raise_for_status()
            logging.info(f"Fetched data for {date_str}")

            soup = BeautifulSoup(response.content, 'html.parser')
            table = soup.find('table', attrs={'id': 'wt-his'})

            if not table:
                logging.warning(f"No table found for {date_str}")
                continue

            temps = []
            for row in table.tbody.find_all('tr'):
                cols = row.find_all('td')
                if len(cols) >= 2:
                    temp_str = cols[1].text.strip()
                    if temp_str.endswith('°C'):
                        try:
                            temp = int(temp_str.replace('°C', '').strip())
                            temps.append(temp)
                        except ValueError as ve:
                            logging.warning(f"ValueError while parsing temperature on {date_str}: {ve}")

            if temps:
                max_temp = max(temps)
                min_temp = min(temps)
                weather_data.append({
                    'Date': date_str,
                    'Max Temperature (°C)': max_temp,
                    'Min Temperature (°C)': min_temp
                })
                logging.info(f"Processed {date_str}: Max={max_temp}, Min={min_temp}")
            else:
                logging.warning(f"No temperature data available for {date_str}")

        except requests.exceptions.HTTPError as http_err:
            logging.error(f"HTTP error for {date_str}: {http_err}")
        except requests.exceptions.RequestException as req_err:
            logging.error(f"Request error for {date_str}: {req_err}")
        except Exception as e:
            logging.error(f"Unexpected error for {date_str}: {e}")

    # Write to CSV
    try:
        with open(csv_file_path, 'w', newline='') as csvfile:
            fieldnames = ['Date', 'Max Temperature (°C)', 'Min Temperature (°C)']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for data in weather_data:
                writer.writerow(data)

        logging.info(f"Weather data successfully written to {csv_file_path}")
        print(f"Data has been written to '{csv_file_path}'.")

    except IOError as io_err:
        logging.error(f"File writing error: {io_err}")
    except Exception as e:
        logging.error(f"Unexpected error while writing CSV: {e}")

if __name__ == "__main__":
    fetch_weather_data()
