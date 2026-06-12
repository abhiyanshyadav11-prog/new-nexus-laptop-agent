import subprocess

def close_application(process_name: str):
    try:
        result = subprocess.run(
            ["taskkill", "/F", "/IM", process_name],
            capture_output=True,
            text=True
        )

        return {
            "status": "success",
            "message": result.stdout,
            "error": result.stderr
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }