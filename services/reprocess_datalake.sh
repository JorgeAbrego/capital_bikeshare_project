#!/bin/bash

# This script automates running an Airflow DAG ("final_bike_share_process") for each month in a year. 
# It could be useful for processing historical data, like populating a table with bike share information from previous months.

# Set the name of the target DAG
DAG_NAME="final_bike_share_process"

# Define the year 
year=2023

# Loop through the months from January to December (don't forget leading zeros for months below october)
for month in {01..12}
do
  # Format the year_month variable using the previously defined year
  YEAR_MONTH="${year}${month}"

  echo "Setting Airflow variable for ${YEAR_MONTH}"  
  # Set the year_month variable in Airflow
  airflow variables set year_month ${YEAR_MONTH}

  echo "Executing DAG for ${YEAR_MONTH}"
  # Trigger the DAG manually
  airflow dags trigger -e ${DAG_NAME}

  # Wait a bit before starting the next month to avoid any conflicts
  sleep 30
done

# Delete the year_month variable to allow the DAG to run normally without it
echo "Deleting Airflow variable year_month"
airflow variables delete year_month

echo "Completed triggering DAG for all months."
