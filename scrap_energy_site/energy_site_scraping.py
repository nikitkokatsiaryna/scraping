"""Scraping data from site https://www.easyenergy.com/nl/energietarieven
Get hourly electricity price and save it to csv file"""

import requests
import json
import csv
from datetime import datetime as dt
import datetime
import sys

"""There's an option to call this script from terminal passing one argument 'start_date' in format dd-mm-YYYY
How to call it: python enegry_site_scraping.py 05-04-2023
"""
# print(f'ARG: {type(sys.argv[1])}')
# print(f'ARG: {sys.argv[1]}')

sys.argv = input("Enter the start date (dd-mm-yyyy): ")   # comment this line if the script will call from the terminal
start_date_str = sys.argv # comment this line if the script will call from the terminal
# start_date_str = sys.argv[1]
end_date = (datetime.datetime.strptime(start_date_str, "%d-%m-%Y") + datetime.timedelta(days=1)).date()
start_date = dt.strptime(start_date_str, "%d-%m-%Y").date()

# Construct the URL with the start date as a parameter
url = f"https://mijn.easyenergy.com/nl/api/tariff/getapxtariffs?startTimestamp={start_date}T03%3A00%3A00." \
      f"000Z&endTimestamp={end_date}T03%3A00%3A00.000Z&grouping=&includeVat=true"
print(f'URL: {url}')

response = requests.get(url)
whole_day_data = json.loads(response.content)

# Extract the hourly energy price data and store it in a list
prices = []
for one_hour in whole_day_data:
    date_time = one_hour['Timestamp']
    rounded_price = round(one_hour['TariffUsage'], 5)
    price = "{:.5f}".format(rounded_price)
    parsed_time = dt.strptime(date_time, "%Y-%m-%dT%H:%M:%S%z").time()
    parsed_date = dt.strptime(date_time, "%Y-%m-%dT%H:%M:%S%z").date()

    # Subtract three hours from the time
    datetime_obj = dt.combine(parsed_date, parsed_time) - datetime.timedelta(hours=3)
    result_date = dt.strftime((datetime_obj).date(), '%d-%m-%Y')
    result_time = str(datetime_obj.time())

    prices.append((result_date, result_time, price))

# Create a CSV file to store the data
csv_file = open('energy_prices.csv', 'w', newline='')
csv_writer = csv.writer(csv_file)

# Write the header row to the CSV file
csv_writer.writerow(['Date', 'Time', 'Price (€/kWh)'])

# Write the data to the CSV file
for date, time, price in prices:
    csv_writer.writerow([date, time, price])

# Close the CSV file
csv_file.close()
