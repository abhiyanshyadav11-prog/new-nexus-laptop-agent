WEBSITES = [
    "youtube",
    "google",
    "github",
    "chatgpt"
]

def parse_command(text):

    text = text.lower().strip()

    # Lock
    if text in ["lock", "lock pc", "lock laptop", "lock system"]:
      return {
        "command": "system_control",
        "args": {
            "action": "lock"
        }
      }

    # Volume
    if text.startswith("volume "):

        try:
            level = int(text.replace("volume ", ""))

            return {
                "command": "audio_control",
                "args": {
                    "level": level
                }
            }

        except:
            pass

    # Find File
    if text.startswith("find "):

        query = text.replace("find ", "")

        return {
            "command": "find_file",
            "args": {
                "query": query
            }
        }

    # Open Something
    if text.startswith("open "):

        item = text.replace("open ", "")

        if item in WEBSITES:
            return {
                "command": "open_website",
                "args": {
                    "site": item
                }
            }

        return {
            "command": "open_app",
            "args": {
                "app_name": item
            }
        }

    return None