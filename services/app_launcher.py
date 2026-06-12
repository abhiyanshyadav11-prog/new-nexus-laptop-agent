import subprocess
from services.app_registry import APPS_PATHS

def open_application(app_name: str):
    app_name = app_name.lower()

    if app_name not in APPS_PATHS:
        return {
            "status": "error",
            "message": f"{app_name} not registered"
        }

    subprocess.Popen(APPS_PATHS[app_name])

    return {
        "status": "success",
        "message": f"Opened {app_name}"
    }