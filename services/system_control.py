import ctypes

def lock_pc():
    try:
        ctypes.windll.user32.LockWorkStation()

        return {
            "status": "success",
            "message": "PC locked"
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }