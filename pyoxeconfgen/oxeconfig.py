import requests
import sys


def oxe_authenticate(ip_address, login, password):
    get_auth = requests.get('https://' + ip_address + '/api/mgt/1.0/login', timeout=10, auth=(login, password),
                            verify=False)
    if 'errorCode' in get_auth.json() and get_auth.json()['errorCode'] == 401:
        print("Authentication failed")
        sys.exit(1)
    return get_auth.json()['token']


def oxe_get_json_model(ip_address):
    return requests.get('https://' + ip_address + '/api/mgt/1.0/Node/1/model')


def oxe_create_user(ip_address, extension, name, first_name, station_type, header_post):
    data_post_create_user = {
        "Annu_Name": name,
        "Annu_First_Name": first_name,
        "Station_Type": station_type
    }
    return requests.post('https://' + ip_address + '/api/mgt/1.0/Node/1/Subscriber/' + str(extension),
                         headers=header_post, json=data_post_create_user, verify=False)
