"""Summary"""
import pprint
import paramiko


def oxe_reboot(host, port, login, password, swinst_password):
    """Summary

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
    stdin, stdout, stderr = client.exec_command('reboot')
    pprint.pprint(stdout.readlines())
    pprint.pprint(stderr.readlines())
    stdin.write(swinst_password + '\n')
    client.close()
