import os
from src.deviceIPCheck import deviceIPcheck
from src.deviceCharacter import showCharacter, closeWindow
from src.deviceVoice import playVoice

# Dummy Test
character = "jjangu"
image_path = "./img/" + character + ".png"
wav_file_path = "./voice/" + character + ".wav"
ip_reader = "ip.mp3"

connected = False
if __name__ == "__main__":
    if not connected:
        default_image_path = "./img/default.png"
        showCharacter(default_image_path)
        deviceIPcheck()

        while os.path.exists(ip_reader):
            connected = False
        connected = True
        closeWindow()

    if connected:
        # TODO: Receive converted voice file
        showCharacter(image_path)
        playVoice(wav_file_path)
        closeWindow()
