
# Nexus Laptop Agent

This is the Python-based laptop agent for the Nexus Pendant ecosystem. It runs locally on your machine and listens for commands from the Nexus mobile app via REST API and WebSockets.

## Features
- Open applications
- Control media playback (play, pause, next, previous)
- Control system volume

## Setup

1.  **Install Python 3.8+**
2.  **Create a virtual environment (optional but recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *Note: Depending on your OS, you might need additional libraries for full functionality (e.g., `pywinauto` for Windows app control, `playerctl` for Linux media control).*

## Running the Agent

```bash
python main.py
```

The agent will start on `http://0.0.0.0:8000`.

## Connecting the Mobile App

1.  Find your laptop's local IP address (e.g., `192.168.1.100`).
2.  In the Nexus mobile app, go to Settings -> Laptop Agent URL.
3.  Enter `http://<your-laptop-ip>:8000`.
4.  Save settings.

## API Endpoints

-   `GET /status`: Check if the agent is running.
-   `POST /command`: Send a command to the agent.
    -   Payload format: `{"command": "action_name", "args": {"key": "value"}}`
-   `WS /ws`: WebSocket endpoint for real-time communication.
