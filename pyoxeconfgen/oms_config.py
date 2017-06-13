"""methods to finalize OMS configuration"""
import pprint
import paramiko
import re
import time


def oms_omsconfig(host, port, login, password, root_password, call_server):
    """Add to oms config CS address, also set Automatic discovery of Crystal number

    Args:
        host (str): OMS IP address / FQDN
        port (str): SSH port for connection
        login (str): Username used for connection
        password (str): Password for connection
        root_password (str): root password

    Returns:
        TYPE: Description
    """
    # connect OXE through SSH and execute 'rainbowagent -v'
    # todo: add more control in checking stuff in stdout
    # todo: find better stuff than while loop to wait recv_ready() state
    client = paramiko.SSHClient()  # use the paramiko SSHClient
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # automatically add SSH key
    try:
        client.connect(host, port, username=login, password=password)
    except paramiko.AuthenticationException:
        print('*** Failed to connect to {}:{}'.format(host, port))
    channel = client.invoke_shell()
    while channel.recv_ready() is False:
        time.sleep(0.1)
    channel.send('su -\n')
    while channel.recv_ready() is False:
        time.sleep(0.1)
    stdout = channel.recv(4096)
    channel.send(root_password + '\n')
    while channel.recv_ready() is False:
        time.sleep(0.1)
    stdout += channel.recv(4096)
    channel.send('omsconfig\n')
    while channel.recv_ready() is False:
        time.sleep(0.1)
    stdout += channel.recv(4096)
    channel.send('2\n')  # view/modify ip info menu
    while channel.recv_ready() is False:
        time.sleep(0.1)
    stdout += channel.recv(4096)
    channel.send('4\n')  # cs main ip address menu
    while channel.recv_ready() is False:
        time.sleep(0.1)
    stdout += channel.recv(4096)
    channel.send(call_server + '\n')
    while channel.recv_ready() is False:
        time.sleep(0.1)
    stdout += channel.recv(4096)
    channel.send('0\n')  # back previous menu
    while channel.recv_ready() is False:
        time.sleep(0.1)
    stdout += channel.recv(4096)
    channel.send('3\n')  # crystal menu
    while channel.recv_ready() is False:
        time.sleep(0.1)
    stdout += channel.recv(4096)
    if re.search('Current mode is: MANUAL', stdout.decode('utf-8')):
        channel.send('2\n')  # set crystal to automatic discovery if current mode is manual
        while channel.recv_ready() is False:
            time.sleep(0.1)
        stdout += channel.recv(4096)
    channel.send('0\n')  # back to previous menu
    while channel.recv_ready() is False:
        time.sleep(0.1)
    stdout += channel.recv(4096)
    channel.send('0\n')  # back to previous menu
    while channel.recv_ready() is False:
        time.sleep(0.1)
    stdout += channel.recv(4096)
    channel.send('y\n')  # save config
    while channel.recv_ready() is False:
        time.sleep(0.1)
    stdout += channel.recv(4096)
    channel.send('y\n')  # reboot
    while channel.recv_ready() is False:
        time.sleep(0.1)
    stdout += channel.recv(4096)
    channel.close()
    client.close()
