# Energy Data ETL

This project is an ETL pipeline for U.S. electricity retail sales data from the EIA API.  
Currently, the project consists of a Python script that extracts, transforms, and loads data into an AWS S3 data lake over the course of several months. The data can later be analyzed using tools like AWS Athena to explore trends.

---

## Project Overview

The pipeline pulls recent electricity consumption and pricing data from the EIA API, cleans and formats it, and stores both the raw and processed data in S3.  

Current functionality:
- Extracts data from the EIA API.
- Cleans and normalizes JSON data using Pandas.
- Uploads raw and cleaned data to separate S3 folders with timestamped filenames.

Future improvements:
- Automate the ETL process with Airflow or another scheduler.
- Add logging and error handling.
- Explore additional EIA datasets.
- Integrate with BI tools like Power BI or Tableau for visualization.

---

## Tech Stack

- Python 3.12  
- Libraries: `pandas`, `requests`, `boto3`, `dotenv`, `json`, `io`  
- Cloud: AWS S3 (data lake)  
- Data Source: [EIA Retail Sales API](https://www.eia.gov/opendata/)

---

## How It Works

1. **Extract**: Requests recent electricity retail sales data from the EIA API.
2. **Transform**: Normalizes JSON responses into a clean Pandas DataFrame.
3. **Load**: Saves the raw JSON and cleaned CSV to S3 with timestamps in separate folders:
   - `raw_eia/` for raw API responses
   - `clean_eia/` for cleaned CSV files

---


