# Plex Webhook MQTT Redirector 🎬🔊

A lightweight and efficient webhook for Plex that sends MQTT messages based on media playback events. Enhance your smart home automation by integrating your Plex media server with MQTT-compatible devices and services!

## 🌟 Features

-   Listens for Plex webhook events (play, pause, resume, stop)
-   Filters events based on media type (movies and episodes)
-   Supports local player filtering
-   Sends corresponding MQTT messages to a specified broker and topic
-   Easily deployable via Docker
-   Configurable through environment variables

## 🚀 Quick Start

1. **Clone the repository:**

    ```bash
    git clone https://github.com/harperreed/plex-webhook-mqtt-redirector.git
    cd plex-webhook-mqtt-redirector
    ```

2. **Set up environment variables:**
   Create a `.env` file in the project root and add your configuration:

    ```
    MQTT_BROKER=your_mqtt_broker_address
    MQTT_TOPIC=your_mqtt_topic
    MQTT_PORT=1883
    TRACKED_PLAYER_UUIDS=uuid1,uuid2,uuid3
    LOCAL_PLAYERS_ONLY=true
    FLASK_PORT=8765
    LOG_FILE=/app/logs/plex_webhook_redirector.log
    ```

3. **Run with Docker Compose:**

    ```bash
    docker-compose up --build
    ```

4. **Configure Plex Webhook:**
   In your Plex server settings, add a new webhook with the URL:
    ```
    http://your_server_ip:8765
    ```

## 🛠 Configuration

-   `MQTT_BROKER`: Address of your MQTT broker
-   `MQTT_TOPIC`: MQTT topic to publish messages to
-   `MQTT_PORT`: Port of your MQTT broker (default: 1883)
-   `TRACKED_PLAYER_UUIDS`: Comma-separated list of Plex player UUIDs to track (optional)
-   `LOCAL_PLAYERS_ONLY`: Set to "true" to only process events from local players
-   `FLASK_PORT`: Port for the Flask application (default: 8765)
-   `LOG_FILE`: Path to the log file

## 📊 Logging

Logs are written to the specified `LOG_FILE` and to the console. They include detailed information about received webhooks and MQTT message status.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📜 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgements

-   Original concept by [Bailey Belvis](https://github.com/philosowaffle)
-   Refactored and maintained by [Harper Reed](https://github.com/harperreed)

For more information or to report issues, please visit the [GitHub repository](https://github.com/harperreed/plex-webhook-mqtt-redirector).
