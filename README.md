# MQTT to InfluxDB Bridge

This script subscribes to MQTT topics from The Things Network, decodes incoming messages, and writes relevant sensor data to an InfluxDB database.

## Requirements

- Python 3.7+
- MQTT credentials for The Things Network
- InfluxDB token and config
- `.env` 

## Python Dependencies

Install requirements using pip:

```bash
pip install -r requirements.txt
```

## Environment Variables

Set these in your environment or a `.env` file:

```bash
INFLUXDB_TOKEN=your_influxdb_token
MQTT_USERNAME=your_ttn_username
MQTT_PASSWORD=your_ttn_password
```

## Script Overview

- Connects to the TTN MQTT broker.
- Subscribes to all topics (`#`).
- Filters out messages from port 69.
- Expects sensor measurements in `decoded_payload.measurements`.
- Maps measurement keys like `t` to `temperature`, `h` to `humidity`, etc.
- Writes structured data points into InfluxDB.

## Customization

- Update the `name_map` dictionary to support more sensor types.
- Modify the InfluxDB `bucket`, `org`, or `url` as needed.

## Running the Script

```bash
python your_script.py
```

Press `Ctrl+C` to stop.

## Notes

- InfluxDB writes are synchronous by default.
- Ensure your device payload structure matches expectations.