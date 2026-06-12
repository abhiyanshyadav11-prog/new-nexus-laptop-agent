
import os
import platform
import subprocess
import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from typing import Optional, Dict, Any
import logging
import psutil

# Configure logging
logging.basicConfig(level=logging.INFO, format="[%(asctime)s] [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(title="Nexus Laptop Agent", description="Agent to control laptop functions from Nexus Pendant")

class Command(BaseModel):
    command: str
    args: Optional[Dict[str, Any]] = None

@app.get("/status")
async def get_status():
    logger.info("Received status request")
    return {"status": "running", "platform": platform.system(), "version": "1.0.0"}

@app.post("/command")
async def execute_command(cmd: Command):
    logger.info(f"Received command: {cmd.command} with args: {cmd.args}")
    response = {"status": "success", "message": "Command executed"}

    try:
        if cmd.command == "open_app":
            app_name = cmd.args.get("app_name")
            if app_name:
                open_application(app_name)
                response["message"] = f"Opened {app_name}"
            else:
                response["status"] = "error"
                response["message"] = "App name not provided"
        elif cmd.command == "media_control":
            action = cmd.args.get("action")
            query = cmd.args.get("query")
            if action:
                media_control(action, query)
                response["message"] = f"Media control: {action}"
            else:
                response["status"] = "error"
                response["message"] = "Media action not provided"
        elif cmd.command == "system_control":
            action = cmd.args.get("action")
            if action == "volume_up":
                set_volume(up=True)
                response["message"] = "Volume increased"
            elif action == "volume_down":
                set_volume(down=True)
                response["message"] = "Volume decreased"
            else:
                response["status"] = "error"
                response["message"] = "System action not supported"
        else:
            response["status"] = "error"
            response["message"] = "Unknown command"
    except Exception as e:
        logger.error(f"Error executing command {cmd.command}: {e}")
        response["status"] = "error"
        response["message"] = str(e)

    return response

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    logger.info("WebSocket connected")
    try:
        while True:
            data = await websocket.receive_text()
            logger.info(f"WebSocket received: {data}")
            await websocket.send_text(f"Message text was: {data}")
    except WebSocketDisconnect:
        logger.info("WebSocket disconnected")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")


def open_application(app_name: str):
    system = platform.system()
    if system == "Windows":
        # This is a placeholder. Real implementation would use pywinauto or similar.
        subprocess.Popen(["start", app_name], shell=True)
    elif system == "Darwin": # macOS
        subprocess.Popen(["open", "-a", app_name])
    elif system == "Linux":
        subprocess.Popen([app_name.lower()]) # Assumes app_name is the command to run
    else:
        raise NotImplementedError(f"Application opening not supported on {system}")
    logger.info(f"Attempted to open application: {app_name}")

def media_control(action: str, query: Optional[str] = None):
    system = platform.system()
    if system == "Windows":
        # Placeholder: Windows media control is complex, often requires COM objects or specific libraries
        if action == "play":
            logger.warning("Windows media play not implemented directly. Consider using a specific media player API.")
        elif action == "pause":
            logger.warning("Windows media pause not implemented directly.")
        elif action == "next":
            logger.warning("Windows media next not implemented directly.")
        elif action == "previous":
            logger.warning("Windows media previous not implemented directly.")
    elif system == "Darwin": # macOS
        if action == "play" and query:
            # Example: open Spotify and play a song (requires Spotify URI)
            subprocess.run(["osascript", "-e", f'tell application \"Spotify\" to play track \"spotify:search:{query}\"
                                                  activate application \"Spotify\"'])
        elif action == "play":
            subprocess.run(["osascript", "-e", "tell application \"Spotify\" to play"]) # Play/Pause toggle
        elif action == "pause":
            subprocess.run(["osascript", "-e", "tell application \"Spotify\" to pause"]) # Play/Pause toggle
        elif action == "next":
            subprocess.run(["osascript", "-e", "tell application \"Spotify\" to next track"]) # Next track
        elif action == "previous":
            subprocess.run(["osascript", "-e", "tell application \"Spotify\" to previous track"]) # Previous track
    elif system == "Linux":
        # Placeholder: Linux media control often uses MPRIS D-Bus interface
        if action == "play":
            subprocess.run(["playerctl", "play"])
        elif action == "pause":
            subprocess.run(["playerctl", "pause"])
        elif action == "next":
            subprocess.run(["playerctl", "next"])
        elif action == "previous":
            subprocess.run(["playerctl", "previous"])
    else:
        raise NotImplementedError(f"Media control not supported on {system}")
    logger.info(f"Attempted media control: {action}")

def set_volume(up: bool = False, down: bool = False):
    system = platform.system()
    if system == "Windows":
        # Placeholder: Windows volume control requires pycaw or similar
        logger.warning("Windows volume control not implemented directly. Consider using pycaw.")
    elif system == "Darwin": # macOS
        if up:
            subprocess.run(["osascript", "-e", "set volume output volume (output volume of (get volume settings) + 10)"])
        elif down:
            subprocess.run(["osascript", "-e", "set volume output volume (output volume of (get volume settings) - 10)"])
    elif system == "Linux":
        if up:
            subprocess.run(["amixer", "-D", "pulse", "sset", "Master", "5%+"])
        elif down:
            subprocess.run(["amixer", "-D", "pulse", "sset", "Master", "5%-"])
    else:
        raise NotImplementedError(f"Volume control not supported on {system}")
    logger.info(f"Attempted volume control: up={up}, down={down}")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
