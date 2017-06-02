import configparser
import pprint
import requests
import requests.packages
import sys
import time
import os
import json
import paramiko


# create connection config file
def configure(host, login, password, proxies):
    directory = 'etc/'
    filename = 'pyoxeconfgen.ini'
    try:
        os.stat(directory)
    except IOError:
        os.mkdir(directory, 0o600)
    config = configparser.RawConfigParser()
    config.add_section('default')
    config.set('default', 'host', str(host))
    config.set('default', 'login', str(login))
    config.set('default', 'password', str(password))
    if proxies is not None:
        config.add_section('proxies')
        config.set('proxies', 'proxies', proxies)
    with open(str(directory + filename), 'w+') as config_file:
        config.write(config_file)


# get connection info from config file
def get_config():
    config = configparser.ConfigParser()
    config.read('etc/pyoxeconfgen.ini')
    oxe_ip = config.get('default', 'host', raw=False)
    login = config.get('default', 'login', raw=False)
    password = config.get('default', 'password', raw=False)
    if config.has_section('proxies'):
        proxies = config.get('proxies', 'proxies', raw=True)
    else:
        proxies = None
    return oxe_ip, login, password, proxies


# store authentication token
def get_auth_from_cache():
    try:
        with open('/tmp/.pyoxeconfgen') as fh:
            tmp = json.loads(fh.read())
            token = tmp['token']
            ip_address = tmp['oxe_ip']
            return token, ip_address
    except IOError:
        print('Please login to go on !!!')
        exit(1)


# build header
def set_headers(token, method=None):
    # basic method GET
    headers = {
        'Authorization': 'Bearer ' + token,
        'accept': 'application/json'
    }
    # addition for POST & PUT
    if method in ('POST', 'PUT'):
        headers.update({'Content-Type': 'application/json'})
    elif method == 'DELETE':
        headers.update({'Content-Type': 'text/plain'})
    return headers


# OXE WBM authentication + JWT cache creation
def oxe_authenticate(host, login, password, proxies=None):
    requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
    get_auth_infos = requests.get('https://' + host + '/api/mgt/1.0/login',
                                  timeout=10,
                                  auth=(login, password),
                                  verify=False,
                                  proxies=proxies)
    if get_auth_infos.status_code == 401:
        print("Error {} - {}".format(get_auth_infos.json()['errorCode'],
                                     get_auth_infos.json()['errorMsg']))
        sys.exit(1)
    token = get_auth_infos.json()['token']
    data = {'oxe_ip': host, 'token': token}
    with open('/tmp/.pyoxeconfgen', 'w') as fh:
        fh.write(json.dumps(data))
    return get_auth_infos.json()['token']  # remove this line when provisioning updated with get_auth_from_cache


# OXE WBM logout + clear JWT cache
def oxe_logout(host, token, proxies=None):
    # clear cache
    try:
        os.remove('/tmp/.pyoxeconfgen')
    except IOError:
        print('JWT cache already purged')
    # close authentication
    requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
    logout = requests.get('https://' + host + '/api/mgt/1.0/logout',
                          headers=set_headers(token),
                          verify=False,
                          proxies=proxies)
    pprint.pprint(logout.status_code)
    # if logout.status_code == 200:
    #     return logout.json()
    # return {'errorCode': logout.status_code}


def oxe_get_json_model(host, token):
    requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
    response = requests.get('https://' + host + '/api/mgt/1.0/model',
                            headers=set_headers(token),
                            verify=False,
                            stream=True)
    result = ''
    for chunk in response.iter_content(chunk_size=1024):
        if chunk:
            result += chunk.decode('utf-8')
    return result


def oxe_set_flex(host, token, flex_ip_address, flex_port):
    requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
    payload = {
        "Flex_Licensing_Enable": "Yes",
        "Flex_Server_Address": flex_ip_address,
        "Flex_Server_Port": flex_port,
        "Flex_ProductId_Discovery": "Yes"
    }
    response = requests.put('https://' + host + '/api/mgt/1.0/Node/1/System_Parameters/1/Flex_Server/1',
                            headers=set_headers(token, 'PUT'),
                            json=payload,
                            verify=False)
    # todo: manage errors
    return response


def oxe_create_user(host, token, extension, last_name, first_name, station_type, max_retries):
    requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
    data_post_create_user = {
        "Annu_Name": last_name,
        "Annu_First_Name": first_name,
        "Station_Type": station_type
    }
    for i in range(max_retries):
        response = requests.post('https://' + host + '/api/mgt/1.0/Node/1/Subscriber/' + str(extension),
                                 headers=set_headers(token, 'POST'),
                                 json=data_post_create_user,
                                 verify=False)
        # code status 201: CREATED
        if response.status_code in (201, 401):
            break
        # code status 503: retry with same requests + wait 500ms (oxe max 2r/s)
        elif response.status_code == 503:
            time.sleep(.500)
    # return response.status_code


def oxe_delete_user(host, token, extension, max_retries):
    requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
    for i in range(max_retries):
        response = requests.delete('https://' + host + '/api/mgt/1.0/Node/1/Subscriber/' + str(extension),
                                   headers=set_headers(token, 'DELETE'),
                                   verify=False)
        # code status 200: OK
        if response.status_code in (200, 404):
            break
        # code status 503: retry with same requests + wait 500ms (oxe max 2r/s)
        elif response.status_code == 503:
            time.sleep(.500)
    # return response.status_code


def oxe_get_rainbow_config():
    config = configparser.ConfigParser()
    config.read('etc/oxe.ini')
    rainbow_domain = config.get('default', 'rainbow_domain', raw=False)
    pbx_id = config.get('default', 'pbx_id', raw=False)
    rainbow_temp_password = config.get('default', 'rainbow_temp_password', raw=False)
    rainbow_host = config.get('default', 'rainbow_host', raw=False)
    return rainbow_domain, pbx_id, rainbow_temp_password, rainbow_host


def oxe_get_rainbow_agent_version(host, port, login, password):
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


def oxe_update_ccca_cfg(host, port, login, password, api_server):
    # update ccca.cfg for all-in-one connection
    client = paramiko.SSHClient()  # use the paramiko SSHClient
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # automatically add SSH key
    try:
        client.connect(host, port, username=login, password=password)
    except paramiko.AuthenticationException:
        print('*** Failed to connect to {}:{}'.format(host, port))
    command = """
    cat >> /usr3/mao/ccca.cfg << EOF
    RAINBOW_HOST={}
    EOF
    """.format(api_server)
    # print(command)
    client.exec_command(command)
    client.close()


def oxe_get_oxe_version(host, port, login, password):
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
