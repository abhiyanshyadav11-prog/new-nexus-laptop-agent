from pycaw.pycaw import AudioUtilities

def set_volume(level):

    devices = AudioUtilities.GetSpeakers()

    volume = devices.EndpointVolume

    volume.SetMasterVolumeLevelScalar(
        float(level) / 100.0,
        None
    )

    return {
        "status": "success",
        "message": f"Volume set to {level}%"
    }