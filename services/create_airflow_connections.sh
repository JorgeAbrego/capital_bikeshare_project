#!/bin/bash

# Wait until Airflow is ready
airflow db check

# Create connection to Google Cloud
airflow connections add 'google_cloud_default' \
    --conn-type 'google_cloud_platform' \
    --conn-extra '{
        "extra__google_cloud_platform__project": ${GCP_PROJECT_ID},
        "extra__google_cloud_platform__key_path": ${GOOGLE_APPLICATION_CREDENTIALS}
    }'