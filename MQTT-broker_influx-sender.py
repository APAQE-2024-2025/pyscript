import random
from itertools import count

from paho.mqtt import client as mqtt_client
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
import json
import os
from dotenv import load_dotenv

load_dotenv()

bucket = "piBucket"
org = "ac73491f5a717267"
url = "https://influxdb.projectdar.aplab.be/"
broker = 'eu1.cloud.thethings.network'
port = 1883

def subscribe(client: mqtt_client):
    def on_message(msg):
        try:
            payload = msg.payload.decode()
            data = json.loads(payload)
            decoded_payload = data['uplink_message']['decoded_payload']
            print(f"Decoded payload: {decoded_payload}")

            point = influxdb_client.Point("SensorData")
            for key, value in decoded_payload.items():
                point = point.field(key, value)
                print(point)
            write_api.write(bucket=bucket, org=org, record=point)
            print("Data written to InfluxDB")

        except Exception as e:
            print(f"Error processing message: {e}")

    client.subscribe(topic)
    client.on_message = on_message

topic = "v3/ardhi-dar-es-salaam@ttn/devices/bme680-ph-dox-full-sensor-test/up"
client_id = f'python-mqtt-{random.randint(0, 1000)}'

token = os.getenv('INFLUXDB_TOKEN')
username = os.getenv('MQTT_USERNAME')
password = os.getenv('MQTT_PASSWORD')

#password =
#token =
#username =

influx_client = influxdb_client.InfluxDBClient(
    url=url,
    token=token,
    org=org
)

write_api = influx_client.write_api(write_options=SYNCHRONOUS)

def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc, properties):
        if rc == 0:
            print(f"\t  Connected to MQTT  \t")
        else:
            print(f"Failed, return code {rc}")
    client = mqtt_client.Client(client_id=client_id, callback_api_version=mqtt_client.CallbackAPIVersion.VERSION2)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def subscribe(client: mqtt_client):
    def on_message(msg):
        try:
            payload = msg.payload.decode()
            data = json.loads(payload)

            uplink = data.get('uplink_message', {})
            decoded_payload = uplink.get('decoded_payload', {})

            f_port = uplink.get('f_port')
            if f_port == 69:
                print(f"Error: {decoded_payload} (received message from port 69). Skipping message.")
                return

            if not decoded_payload or 'measurements' not in decoded_payload:
                print("Missing 'decoded_payload' or 'measurements' key. Skipping message.")
                return

            name_map = {
                "t": "temperature",
                "h": "humidity",
                "p": "pressure",
                "s": "sulfur"
            }
            measurements = decoded_payload['measurements']
            if not isinstance(measurements, list):
                print("'measurements' is not a list. Skipping message.")
                return

            device_id = data.get('end_device_ids', {}).get('device_id', 'unknown-device')

            point = influxdb_client.Point("SensorData")

            for measurement in measurements:
                original_name = measurement.get('name')
                mapped_name = name_map.get(original_name, original_name)
                value = measurement.get('value')

                if value is not None:
                    point = point.field(mapped_name, value)

            point = point.tag("device_id", device_id)

            # print(f"|\t{count}\t|\t{point}")

            write_api.write(bucket=bucket, org=org, record=point)
            print("Data written to InfluxDB")

        except Exception as e:
            print(f"Error processing message: {e}")

    client.subscribe(topic)
    client.on_message = on_message

def run():
    client = connect_mqtt()
    subscribe(client)
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        print("Interrupted by user. Exiting cleanly.")

if __name__ == '__main__':
    run()