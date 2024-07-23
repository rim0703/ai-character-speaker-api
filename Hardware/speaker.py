import os
from src.deviceIPCheck import deviceIPcheck
from src.deviceCharacter import showCharacter
from src.deviceVoice import playVoice
from preferredsoundplayer import playsound
import time

ip_reader = "ip.mp3"
directory_path = "/home/willtek/lge/voice"

connected = False
if __name__ == "__main__":
    default_image_path = "./img/default.png"
    showCharacter(default_image_path)

    if not connected:
        deviceIPcheck()

        while os.path.exists(ip_reader):
            connected = False
            time.sleep(3)  # 3초에 한번 출력
            playsound(ip_reader)
        connected = True

    while connected:
        time.sleep(3)
        if any(
            os.path.isfile(os.path.join(directory_path, f))
            for f in os.listdir(directory_path)
        ):
            for f in os.listdir(directory_path):
                voice_path = os.path.join(directory_path, f)
                playVoice(voice_path)
                os.remove(voice_path)
                break
        else:
            print("[NO VOICE] waiting for file...")
