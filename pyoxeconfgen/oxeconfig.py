import requests


def authenticate(ipAddr, login, password):
    get_auth = requests.get('https://' + ipAddr + '/api/mgt/1.0/login', timeout=10, auth=(login, password),
                            verify=False)
    if 'errorCode' in get_auth.json() and get_auth.json()['errorCode'] == 401:
        print("Authentication failed")
        sys.exit(1)
    return get_auth.json()['token']


def createUser(ipAddr, extension, name, firstName, stationType, headerPost):
    data_post_create_user = {
        "Annu_Name": name,
        "Annu_First_Name": firstName,
        "Station_Type": stationType
    }
    return requests.post('https://' + ipAddr + '/api/mgt/1.0/Node/1/Subscriber/' + str(extension),
                         headers=headerPost, json=data_post_create_user, verify=False)
