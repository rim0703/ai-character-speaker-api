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
