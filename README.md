# plex-webhook-mqtt-redirector
 🚀

A webhook for Plex that enhances your media experience by altering the color of your LIFX lights to match the main colors of the poster art being played. This innovative integration promises to make your viewing experience more immersive and visually appealing! 🎉

## 📚 Summary of the Project

The **plex-webhook-redirector** integrates seamlessly with your Plex media server to control connected smart devices based on media playback events. Whether it's playing, pausing, or stopping content, the webhook sends messages to an MQTT broker to trigger compatible devices, like LIFX lights. This refactored version of the original script utilizes MQTT for improved communication and event management, enhancing both functionality and performance.

## 🌟 How to Use

Follow these simple steps to get started:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/harperreed/plex-webhook-redirector.git
   cd plex-webhook-redirector
   ```

2. **Configure Environment Variables**:
   Ensure you set up your environment variables for the application (e.g., `MQTT_BROKER`, `MQTT_TOPIC`, and `FILTERED_PLAYERS` if necessary). Don't forget to restart the script when you make any configuration changes! 🔧

3. **Install Dependencies**:
   Use `requirements.txt` to install the necessary packages:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**:
   You can either run it directly with Python:
   ```bash
   python plex-webhook-redirector.py
   ```
   OR, for Docker users, you can set it up using the provided `docker-compose.yml` file:
   ```bash
   docker-compose up --build
   ```

5. **Add Webhook to Plex**:
   - Navigate to your Plex server settings and add the webhook URL:
     ```
     http://localhost:8765
     ```

## ⚙️ Tech Info

- **Requirements**:
  - A Plex Pass and a server version that supports [Plex Webhooks](https://support.plex.tv/hc/en-us/articles/115002267687-Webhooks)
  - Python 3.9 or higher (as Python 2.7 has been deprecated)

- **Technologies Used**:
  - **Python**: For implementing the webhook logic.
  - **Flask**: Utilizing this micro web framework to handle HTTP requests.
  - **MQTT**: For sending real-time messages to connected devices.
  - **Docker**: For containerization to simplify deployment and dependency management.

- **Directory Structure**:
  ```
  plex-webhook-redirector/
  ├── Dockerfile
  ├── README.md
  ├── docker-compose.yml
  ├── plex-webhook-redirector.py
  └── requirements.txt
  ```

- **File Descriptions**:
  - `Dockerfile`: Instructions for building the Docker container.
  - `docker-compose.yml`: Defines the service for easy deployment using Docker.
  - `plex-webhook-redirector.py`: The primary script that processes Plex webhooks and triggers MQTT messages.
  - `requirements.txt`: Lists all the required Python packages.

---

Feel free to contribute, start discussions, report issues, or request features! 🌈 

For any additional information or questions, you can reach out to me here on GitHub: [harperreed](https://github.com/harperreed). Happy coding! 💻✨
