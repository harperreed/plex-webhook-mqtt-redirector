# pplex-webhook-mqtt-redirector 🚀

A webhook for Plex that alters the color of your LIFX lights to match the main colors of the poster art being played. This can enhance your media experience, making it more immersive and visually appealing.

## 📚 Summary of the Project

The **plex-webhook-redirector** is designed to work with your Plex media server to control connected devices based on the media playback events. When an event occurs (play, pause, etc.), the webhook sends a message to an MQTT broker, which can trigger compatible smart devices, such as LIFX lights. This project is a refactored version of the original script, utilizing MQTT for better communication and event handling.

## 🌟 How to Use

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/harperreed/plex-webhook-redirector.git
   cd plex-webhook-redirector
   ```

2. **Configure Environment Variables**:
   Set up your environment variables for the application (e.g., `MQTT_BROKER`, `MQTT_TOPIC`, `FILTERED_PLAYERS` if needed). Make sure to restart the script after any configuration changes.

3. **Install Dependencies**:
   Install the necessary packages via requirements.txt:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**:
   You can either run it directly with Python:
   ```bash
   python plex_webhook_redirector.py
   ```
   or you can set it up using Docker with the provided `docker-compose.yml` file.
   ```bash
   docker-compose up --build
   ```

5. **Add Webhook to Plex**:
   - Go to your Plex server settings and add the webhook URL:
     ```
     http://localhost:8765
     ```

## ⚙️ Tech Info

- **Requirements**:
  - Plex Pass and Server version that supports [Plex Webhooks](https://support.plex.tv/hc/en-us/articles/115002267687-Webhooks)
  - Python 3.9+ (Python 2.7 has been deprecated and Python 3 is recommended)

- **Technologies Used**:
  - **Python** for scripting the webhook logic.
  - **Flask** as the micro web framework for handling requests.
  - **MQTT** for sending real-time messages to your connected devices.
  - **Docker** for containerization, making it easy to deploy and manage dependencies.

- **Directory Structure**:
  ```
  plex-webhook-redirector/
  ├── Dockerfile
  ├── README.md
  ├── docker-compose.yml
  ├── logs
  ├── plex-webhook-redirector.py
  └── requirements.txt
  ```

- **File Descriptions**:
  - `Dockerfile`: Contains instructions for building the Docker container.
  - `docker-compose.yml`: Defines the service for easy deployment using Docker.
  - `plex-webhook-redirector.py`: The main application script that processes Plex webhooks and triggers MQTT messages.
  - `requirements.txt`: Lists necessary Python packages.

Feel free to contribute, report issues, or request features! 🌈

For more information, reach out to me here on GitHub: [harperreed](https://github.com/harperreed). Happy coding! 💻✨
