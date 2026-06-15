from services.app_launcher import open_application
from services.website_launcher import open_website
from services.app_launcher import open_application
from services.website_launcher import open_website
from services.app_registry import APPS_PROCESSES
from services.app_closer import close_application
from services.system_control import lock_pc
from services.file_search import find_file
from services.file_opener import open_file
from services.audio_control import set_volume
from services.command_parser import parse_command
import os
import platform
import subprocess
import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from typing import Optional, Dict, Any
import logging
import psutil
from dotenv import load_dotenv
import os
from fastapi import FastAPI, Header, HTTPException

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")


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
async def execute_command(cmd: Command,  authorization: str = Header(None)):
    logger.info(f"Received command: {cmd.command} with args: {cmd.args}")
    print("TOKEN =", API_TOKEN)
    print("HEADER =", authorization)

    if authorization != f"Bearer {API_TOKEN}":
      raise HTTPException(
               status_code=401,
               detail="Unauthorized"
            )
    
    response = {"status": "success", "message": "Command executed"}

    try:

        if cmd.command == "open_app":
            app_name = cmd.args.get("app_name")

            if app_name:
               return open_application(app_name)

            return {
                  "status": "error",
                  "message": "App name not provided"
        }

        elif cmd.command == "ai_command":

           text = cmd.args.get("text")

           parsed = parse_command(text)

           if not parsed:
              return {
                "status": "error",
                "message": "Could not understand command"
            }

           return await execute_command(
             Command(
                command=parsed["command"],
                args=parsed["args"]
             ),
             authorization=authorization
            )
        
       
        elif cmd.command == "close_app":

           app_name = cmd.args.get("app_name")

           if app_name:
             process = APPS_PROCESSES.get(app_name.lower())
              
             print("APP =", app_name)
             print("PROCESS =", process)

             if process:
                return close_application(process)

             return {
               "status": "error",
               "message": "App not found"
        }
           
        elif cmd.command == "system_control":

            action = cmd.args.get("action")

            if action == "lock":
               return lock_pc()

            return {
               "status": "error",
               "message": "Invalid system action"
        }

        elif cmd.command == "find_file":

            query = cmd.args.get("query")

            if query:
              return find_file(query)

            return {
               "status": "error",
               "message": "Query not provided"
        }

        elif cmd.command == "open_file":

            path = cmd.args.get("path")

            if path:
              return open_file(path)

            return {
               "status": "error",
                "message": "Path not provided"
        }
    
        elif cmd.command == "media_control":
            action = cmd.args.get("action")
            query = cmd.args.get("query")
            if action:
                media_control(action, query)
                response["message"] = f"Media control: {action}"
            else:
                response["status"] = "error"
                response["message"] = "Media action not provided"

        elif cmd.command == "open_website":
            site = cmd.args.get("site") or cmd.args.get("app_name")

            if site:
              return open_website(site)

            return {
               "status": "error",
               "message": "Website not provided"
        }

        elif cmd.command == "audio_control":
           print(cmd.args)
           level = cmd.args.get("level")

           if level is not None:

              result = set_volume(level)

           return {
               "status": "error",
               "message": "Level not provided"
        }
          
        

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
            logger.info(f"Spotify search requested: {query}")
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



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
