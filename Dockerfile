# Use python 3.11 instead of 3.12 due to issue in KCC
# https://github.com/ciromattia/kcc/issues/618

# Using Debian Slim instead of Alpine due to incompatibility
# with some dependencies in requirements.txt and the musl library.
# https://github.com/docker-library/python/issues/678#issuecomment-1013310411

FROM python:3.11-slim-bullseye

# Install build dependencies
RUN apt update
RUN apt install -y git python3-dev python3-pip libpng-dev libjpeg-dev p7zip-full python3-pyqt5

# Grab the actual application and put it in /opt
# Specifically grab the latest version by its tag, because we want
# the latest release, not a dev version.
# Set depth to 1 since we don't need the history.
RUN git clone https://github.com/ciromattia/kcc.git --depth 1 --branch v6.1.0 /opt/kcc

# Install python dependencies
RUN pip3 install -r /opt/kcc/requirements.txt

# Copy this program into the container
COPY run.py /app/

# Define the entrypoint
CMD [ "python3", "/app/run.py" ]