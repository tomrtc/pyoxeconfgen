import requests
import sys
import pprint


def oxe_authenticate(ip_address, login, password):
    get_auth = requests.get('https://' + ip_address + '/api/mgt/1.0/login', timeout=10, auth=(login, password),
                            verify=False)
    if 'errorCode' in get_auth.json() and get_auth.json()['errorCode'] == 401:
        print("Authentication failed")
        sys.exit(1)
    return get_auth.json()['token']


def oxe_get_json_model(ip_address, header_get):
    return requests.get('https://' + ip_address + '/api/mgt/1.0/Node/1/model', headers=header_get, verify=False)


def oxe_set_flex(ip_address, flex_ip_address, flex_port, header_put):
    payload = {
        "Flex_Licensing_Enable": "Yes",
        "Flex_Server_Address": flex_ip_address,
        "Flex_Server_Port": flex_port,
        "Flex_ProductId_Discovery": "Yes"
    }
    return requests.put('https://' + ip_address + '/api/mgt/1.0/Node/1/System_Parameters/1/Flex_Server/1',
                        headers=header_put, json=payload, verify=False)


def oxe_create_user(ip_address, extension, name, first_name, station_type, header_post):
    data_post_create_user = {
        "Annu_Name": name,
        "Annu_First_Name": first_name,
        "Station_Type": station_type
    }
    return requests.post('https://' + ip_address + '/api/mgt/1.0/Node/1/Subscriber/' + str(extension),
                         headers=header_post, json=data_post_create_user, verify=False)
