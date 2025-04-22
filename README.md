
# MQTT to InfluxDB Bridge

This script subscribes to MQTT topics from The Things Network (TTN), decodes incoming messages, and writes relevant sensor data to an InfluxDB database.

## Requirements

- Python 3.7+
- MQTT credentials for The Things Network
- InfluxDB token and configuration
- `.env` file with environment variables

---

## Development Setup (Testing)

### Python Dependencies

Install required packages:

```bash
pip install -r requirements.txt
```

### Environment Variables

Set these in your shell or a `.env` file:

```bash
INFLUXDB_TOKEN=your_influxdb_token
MQTT_USERNAME=your_ttn_username
MQTT_PASSWORD=your_ttn_password
```

### Script Overview

- Connects to the TTN MQTT broker
- Subscribes to all topics (`#`)
- Ignores messages from port `69`
- Expects sensor data in `decoded_payload.measurements`
- Maps short keys (e.g., `t`, `h`) to full names like `temperature`, `humidity`
- Writes structured data into InfluxDB

### Customization

- Extend the `name_map` dictionary for additional sensors
- Adjust InfluxDB config (`bucket`, `org`, `url`) as needed

### Running the Script

```bash
python your_script.py
```

Use `Ctrl+C` to stop.

### Notes

- InfluxDB writes are synchronous by default
- Make sure your device payload matches the expected format

---

## Production Deployment

### Clone the Repository

```bash
git clone git@github.com:APAQE-2024-2025/pyscript.git
```

### Build the Docker Image

```bash
docker compose build
```

### Start the Container

```bash
docker compose up -d
```