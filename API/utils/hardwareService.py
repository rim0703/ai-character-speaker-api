import paramiko


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


async def sendVoiceToHardwareService(host_ip):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    connected = False

    try:
        client.connect(hostname=host_ip, port=22, username="willtek", password="1234")
        sftp = client.open_sftp()
        try:
            sftp.stat("/lge/ip.mp3")  # Not Connected
        except:
            connected = True
    except:
        connected = False

    if connected:
        local_file_path = ""
        remote_file_path = ""
        sftp.put(local_file_path, remote_file_path)
        sftp.close()
        client.close()
        return {"status": "playing"}
    else:
        return {"status": "disconnected"}
