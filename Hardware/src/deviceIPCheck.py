# For Raspberry Pi

import subprocess
from gtts import gTTS
from preferredsoundplayer import playsound


def getDeviceIP():
    try:
        result = subprocess.run(
            ["ip", "-4", "addr", "show", "eth0"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )

        ip_line = next(line for line in result.stdout.split("\n") if "inet " in line)
        ip_address = ip_line.split()[1].split("/")[0]

        return ip_address

    except subprocess.CalledProcessError as e:
        print(f"Command failed with error: {e.stderr}")
    except StopIteration:
        print("No IPv4 address found for eth0")
    except Exception as e:
        print(f"An error occurred: {e}")


def deviceIPcheck():
    ip_address = getDeviceIP()
    text = "IP주소는 " + str(ip_address) + "입니다."
    tts = gTTS(text=text, lang="ko")
    tts.save("ip.mp3")
    playsound("ip.mp3")
