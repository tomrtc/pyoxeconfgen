# import pprint
import requests
import sys
import time


def oxe_authenticate(ip_address, login, password):
    get_auth = requests.get('https://' + ip_address + '/api/mgt/1.0/login', timeout=10, auth=(login, password),
                            verify=False)
    if 'errorCode' in get_auth.json() and get_auth.json()['errorCode'] == 401:
        print("Authentication failed")
        sys.exit(1)
    return get_auth.json()['token']


def oxe_get_json_model(ip_address, header_get):
    response = requests.get('https://' + ip_address + '/api/mgt/1.0/model', headers=header_get, verify=False,
                            stream=True)
    result = ''
    for chunk in response.iter_content(chunk_size=1024):
        if chunk:
            result += chunk.decode('utf-8')
    return result


def oxe_set_flex(ip_address, flex_ip_address, flex_port, header_put):
    payload = {
        "Flex_Licensing_Enable": "Yes",
        "Flex_Server_Address": flex_ip_address,
        "Flex_Server_Port": flex_port,
        "Flex_ProductId_Discovery": "Yes"
    }
    response = requests.put('https://' + ip_address + '/api/mgt/1.0/Node/1/System_Parameters/1/Flex_Server/1',
                            headers=header_put, json=payload, verify=False)
    # todo: manage errors
    return response


def oxe_create_user(ip_address, extension, name, first_name, station_type, header_post, max_retries):
    data_post_create_user = {
        "Annu_Name": name,
        "Annu_First_Name": first_name,
        "Station_Type": station_type
    }
    for i in range(max_retries):
        response = requests.post('https://' + ip_address + '/api/mgt/1.0/Node/1/Subscriber/' + str(extension),
                                 headers=header_post, json=data_post_create_user, verify=False)
        # code status 201: CREATED
        if response.status_code == 201:
            break
        # code status 503: retry with same requests + wait 500ms (oxe max 2r/s)
        else:
            time.sleep(.500)
        return response


def oxe_delete_user(ip_address, extension, header_delete, max_retries):
    for i in range(max_retries):
        response = requests.delete('https://' + ip_address + '/api/mgt/1.0/Node/1/Subscriber/' + str(extension),
                                   headers=header_delete, verify=False)
        # code status 200: OK
        if response.status_code == 200:
            break
        # code status 503: retry with same requests + wait 500ms (oxe max 2r/s)
        else:
            time.sleep(.500)
        return response
