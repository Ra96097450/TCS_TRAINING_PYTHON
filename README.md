# Weather Forecasting Using Python 🌤️

This repository contains my learning journey and final project on **Weather Forecasting**, using historical weather data of Kolkata. The goal was to predict future temperatures using statistical modeling and display the results through a web interface.

## 🧠 Skills Practiced

Before building the main project, I practiced and explored the following core concepts, organized into separate folders:

### 🔥 Flask
- Developed a basic understanding of Python-based web development using Flask.
- Built simple routes, templates with Jinja2, and served predictions on the browser.

### 🍃 MongoDB
- Learned to store and retrieve weather data using MongoDB.
- Used PyMongo to interact with the database and manage data persistence.

### 🔁 Multi-threading and Multi-processing
- Practiced concurrent data processing using Python's `threading` and `multiprocessing` modules.
- Explored performance differences and use-cases for CPU vs I/O-bound operations.

---

## 📊 Weather Forecasting Project

The final project, located inside `Weather_Forecasting_Using_Python`, uses all the above knowledge to:

- **Scrape historical weather data** using BeautifulSoup from timeanddate.com.
- **Store and retrieve** weather data using MongoDB.
- **Train a SARIMA time series model** to predict future temperatures.
- **Display the prediction** (next 10 day's temperature) using a Flask web app.
- **Sending mail** of weather forecasted data to a email address.

### 🔧 Technologies Used
- Python
- Flask
- MongoDB
- Pandas
- Statsmodels (SARIMA)
- BeautifulSoup (Web scraping)

---

## 📁 Project Structure

```bash
TCS_Training/
├── Flask/                          # Flask practice code
├── Mongodb/                        # MongoDB practice scripts
├── Multi Threading and Multiprocessing/  # Practice for concurrency
├── Weather_Forecasting_Using_Python/     # Final integrated project
