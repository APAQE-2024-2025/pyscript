FROM amazonlinux:latest

# Update packages and install necessary dependencies
RUN yum update -y && \
    yum install -y git python3-pip

COPY requirements.txt .
COPY MQTT-broker_influx-sender.py .
COPY .env .

# Install Python dependencies
RUN pip3 install -r requirements.txt

EXPOSE 1883

# Specify the command to run the Python application
CMD ["python3", "-u", "MQTT-broker_influx-sender.py"]
