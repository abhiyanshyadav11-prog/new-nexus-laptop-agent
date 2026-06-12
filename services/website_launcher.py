import webbrowser

WEBSITES = {
    "youtube": "https://youtube.com",
    "google": "https://google.com",
    "github": "https://github.com",
    "chatgpt": "https://chatgpt.com",
}

def open_website(site: str):
    site = site.lower()

    if site not in WEBSITES:
        return {
            "status": "error",
            "message": f"{site} not registered"
        }

    webbrowser.open(WEBSITES[site])

    return {
        "status": "success",
        "message": f"Opened {site}"
    }