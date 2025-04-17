FROM amazonlinux:latest

# Update packages and install necessary dependencies
RUN yum update -y && \
    yum install -y git python3-pip

# Install Python dependencies
RUN pip3 install -r requirements.txt

# Expose port 2000 (if required)
EXPOSE 1883

# Specify the command to run the Python application
CMD ["python3", "./MQTT-broker_influx-sender.py"]