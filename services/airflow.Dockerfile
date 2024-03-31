FROM apache/airflow:slim-2.8.2-python3.10

# When adding packages via apt you should switch to the root user when running the apt commands.
# Switch back to the airflow user after installation is complete

# Adding extra packages
# USER root

# Install Java JRE
# RUN apt-get update \
#   && apt-get install -y --no-install-recommends \
#          openjdk-17-jre \
#   && apt-get autoremove -yqq --purge \
#   && apt-get clean \
#   && rm -rf /var/lib/apt/lists/*

# Install Google Cloud SDK
# RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] http://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.lisoogle Cloud SDK
#     && curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key --keyring /usr/share/keyrings/cloud.google.gpg add oogle Cloud SDK
#     && apt-get update -oogle Cloud SDK
#     && apt-get install google-cloud-sdk -y

# USER airflow

# Copy the requirements file into the Docker container
COPY ["requirements_airflow.txt", "create_airflow_connections.sh", "reprocess_datalake.sh", "./"] 
#COPY --chmod=0755 create_airflow_connections.sh .

# Install dependencies using pip (set global.trusted-host to solve ssl conflicts)
RUN pip install --no-cache-dir --upgrade pip && \
    pip config set global.trusted-host \
    "pypi.org raw.githubusercontent.com pypi.python.org" \
    --trusted-host=pypi.python.org \
    --trusted-host=pypi.org \
    --trusted-host=raw.githubusercontent.com && \
    pip install --no-cache-dir --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-3.10.txt" -r requirements_airflow.txt 

ENV SHELL /bin/bash