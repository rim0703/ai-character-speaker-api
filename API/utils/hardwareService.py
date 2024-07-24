import paramiko
from repository.device import find_all_devices


async def checkHardwareStatusService(host_ip):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(hostname=host_ip, port=22, username="willtek", password="1234")
        sftp = client.open_sftp()
        try:
            sftp.stat("/lge/ip.mp3")  # Not Connected
        except:
            return {"status": "connected"}
        client.close()
    except:
        return {"status": "disconnected"}
    return {"status": "disconnected"}


async def connectToHardwareService(host_ip):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname=host_ip, port=22, username="willtek", password="1234")
        client.exec_command(
            "rm /home/willtek/lge/ip.mp3"  # change connection status (disconnected -> connected)
        )
        sftp = client.open_sftp()
        try:
            sftp.stat("/lge/ip.mp3")  # Not Connected
        except:
            return {"status": "connected"}
        client.close()
    except:
        return {"status": "disconnected"}
    return {"status": "disconnected"}


async def sendVoiceToHardwareService(local_file, file_name):
    device = await find_all_devices()
    host_ip = device[0]["device_ip"]

    connected = False

    try:
        client = paramiko.Transport((host_ip, 22))
        client.connect(username="willtek", password="1234")
        sftp = paramiko.SFTPClient.from_transport(client)
        connected = True
    except:
        connected = False

    if connected:
        local_file_path = local_file
        remote_file_path = "/home/willtek/lge/voice/" + file_name
        sftp.put(local_file_path, remote_file_path)
        sftp.close()
        client.close()
        return {"status": "playing"}
    else:
        return {"status": "disconnected"}
