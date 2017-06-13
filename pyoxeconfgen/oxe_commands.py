"""Summary"""
import paramiko
import time
import re
import pprint


def oxe_reboot(host, port, login, password, swinst_password):
    """Reboot OXE Call Server

    Args:
        host (TYPE): Description
        port (TYPE): Description
        login (TYPE): Description
        password (TYPE): Description
        swinst_password (TYPE): Description

    Returns:
        TYPE: Description
    """
    # connect OXE through SSH and execute 'rainbowagent -v'
    client = paramiko.SSHClient()  # use the paramiko SSHClient
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # automatically add SSH key
    try:
        client.connect(host, port, username=login, password=password)
    except paramiko.AuthenticationException:
        print('*** Failed to connect to {}:{}'.format(host, port))
    channel = client.invoke_shell()
    while channel.recv_ready() is False:
        time.sleep(3)  # OXE is really slow on mtcl connexion
    stdout = channel.recv(4096)
    channel.send('reboot\n')
    while channel.recv_ready() is False:
        time.sleep(1)
    stdout += channel.recv(1024)
    channel.send(swinst_password + '\n')
    while channel.recv_ready() is False:
        time.sleep(0.5)
    stdout += channel.recv(1024)
    channel.close()
    client.close()
