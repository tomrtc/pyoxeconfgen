""" OXE Shelves configuration methods """
import pprint
import requests
import requests.packages
from pyoxeconfgen.oxe_access import oxe_set_headers


# Create shelves
def oxe_create_shelf(host, token, shelf_id, rack_size):
    payload = {
        'Rack_Size': rack_size
    }
    if id == 0 or id == 18 or id ==19:
        print('Error can\'t proceed to create shelf with reserved id : {}'.format(id))
        exit(-1)
    requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
    creation = requests.post('https://' + host + '/api/mgt/1.0/Node/1/Rack/' + str(shelf_id),
                             json=payload,
                             headers=oxe_set_headers(token, 'POST'),
                             verify=False)
    pprint.pprint(creation.json())


# Update shelf ethernet parameters
def oxe_shelf_ethernet_parameters(host, token, shelf_id, mac_address):
    payload = {
        'Board_Ethernet_Address': mac_address
    }
    requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
    creation = requests.put('https://' + host + 'api/mgt/1.0/Node/1/Rack/' + str(shelf_id)
                            + '/Board/0/Ethernet_Parameters/' + str(shelf_id) + '-0',
                            json=payload,
                            headers=oxe_set_headers(token, 'PUT'),
                            verify=False)
    pprint.pprint(creation.json())
