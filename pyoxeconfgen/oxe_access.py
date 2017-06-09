""" OXE connection methods """
import configparser
import pprint
import requests
import requests.packages
import sys
import os
import json


# create connection config file
def oxe_configure(host, login, password, proxies):
    """Create config file with OXE connection parameters

    Args:
        host (str): OXE IP or FQDN
        login (str): mtcl user
        password (str): Description
        proxies (json): Description
    """
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
def oxe_get_config():
    """Summary

    Returns:
        TYPE: Description
    """
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
def oxe_get_auth_from_cache():
    """Summary

    Returns:
        TYPE: Description
    """
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
def oxe_set_headers(token, method=None):
    """Summary

    Args:
        token (TYPE): Description
        method (None, optional): Description

    Returns:
        TYPE: Description
    """
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
    """Summary

    Args:
        host (TYPE): Description
        login (TYPE): Description
        password (TYPE): Description
        proxies (None, optional): Description

    Returns:
        TYPE: Description
    """
    requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
    authentication = requests.get('https://' + host + '/api/mgt/1.0/login',
                                  timeout=10,
                                  auth=(login, password),
                                  verify=False,
                                  proxies=proxies)
    if authentication.status_code == 401:
        print('Error {} - {}'.format(authentication.json()['errorCode'],
                                     authentication.json()['errorMsg']))
        sys.exit(-1)
    elif authentication.status_code == 000:
        print('Error {} - telephony is not running on OXE / WBM not available'.format(authentication.status_code))
        sys.exit(-1)
    token = authentication.json()['token']
    data = {'oxe_ip': host, 'token': token}
    with open('/tmp/.pyoxeconfgen', 'w') as fh:
        fh.write(json.dumps(data))
    return authentication.json()['token']  # remove this line when provisioning updated with get_auth_from_cache


# OXE WBM logout + clear JWT cache
def oxe_logout(host, token, proxies=None):
    """Summary

    Args:
        host (TYPE): Description
        token (TYPE): Description
        proxies (None, optional): Description
    """
    # clear cache
    try:
        os.remove('/tmp/.pyoxeconfgen')
    except IOError:
        print('JWT cache already purged')
    # close authentication
    requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
    logout = requests.get('https://' + host + '/api/mgt/1.0/logout',
                          headers=oxe_set_headers(token),
                          verify=False,
                          proxies=proxies)
    pprint.pprint(logout.status_code)
    # if logout.status_code == 200:
    #     return logout.json()
    # return {'errorCode': logout.status_code}
