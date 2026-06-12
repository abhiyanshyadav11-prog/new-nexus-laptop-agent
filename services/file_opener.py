import os

def open_file(path: str):

    try:
        os.startfile(path)

        return {
            "status": "success",
            "message": f"Opened {path}"
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }