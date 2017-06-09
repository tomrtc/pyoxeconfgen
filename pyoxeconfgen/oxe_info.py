""" OXE infos methods """
import pprint
import requests
import requests.packages
import paramiko
from pyoxeconfgen.oxe_access import oxe_set_headers


def oxe_get_json_model(host, token):
    """Summary

    Args:
        host (TYPE): Description
        token (TYPE): Description

    Returns:
        TYPE: Description
    """
    requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
    response = requests.get('https://' + host + '/api/mgt/1.0/model',
                            headers=oxe_set_headers(token),
                            verify=False,
                            stream=True)
    result = ''
    for chunk in response.iter_content(chunk_size=1024):
        if chunk:
            result += chunk.decode('utf-8')
    return result


def oxe_get_rainbow_agent_version(host, port, login, password):
    """Summary

    Args:
        host (TYPE): Description
        port (TYPE): Description
        login (TYPE): Description
        password (TYPE): Description

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
    command = 'rainbowagent -v'
    stdin, stdout, stderr = client.exec_command(command)
    version = {'rainbowagent version': stdout.readlines()[0].split()[2]}
    pprint.pprint(version)
    client.close()
    return version


def oxe_get_oxe_version(host, port, login, password):
    """Summary

    Args:
        host (TYPE): Description
        port (TYPE): Description
        login (TYPE): Description
        password (TYPE): Description

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
    command = 'siteid'
    stdin, stdout, stderr = client.exec_command(command)
    tmp = stdout.readlines()
    version = {'OXE version': tmp[2].split()[4].upper() + '.' + tmp[3].split()[3]}
    pprint.pprint(version)
    client.close()
    return version
