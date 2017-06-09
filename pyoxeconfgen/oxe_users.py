"""Summary"""
import requests
import requests.packages
import time
from pyoxeconfgen.oxe_access import oxe_set_headers


def oxe_create_user(host, token, extension, last_name, first_name, station_type, max_retries):
    """Summary

    Args:
        host (TYPE): Description
        token (TYPE): Description
        extension (TYPE): Description
        last_name (TYPE): Description
        first_name (TYPE): Description
        station_type (TYPE): Description
        max_retries (TYPE): Description
    """
    requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
    payload = {
        "Annu_Name": last_name,
        "Annu_First_Name": first_name,
        "Station_Type": station_type
    }
    for i in range(max_retries):
        response = requests.post('https://' + host + '/api/mgt/1.0/Node/1/Subscriber/' + str(extension),
                                 headers=oxe_set_headers(token, 'POST'),
                                 json=payload,
                                 verify=False)
        # code status 201: CREATED
        if response.status_code in (201, 401):
            break
        # code status 503: retry with same requests + wait 500ms (oxe max 2r/s)
        elif response.status_code == 503:
            time.sleep(.500)
            # return response.status_code


def oxe_delete_user(host, token, extension, max_retries):
    """Summary

    Args:
        host (TYPE): Description
        token (TYPE): Description
        extension (TYPE): Description
        max_retries (TYPE): Description
    """
    requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
    for i in range(max_retries):
        response = requests.delete('https://' + host + '/api/mgt/1.0/Node/1/Subscriber/' + str(extension),
                                   headers=oxe_set_headers(token, 'DELETE'),
                                   verify=False)
        # code status 200: OK
        if response.status_code in (200, 404):
            break
        # code status 503: retry with same requests + wait 500ms (oxe max 2r/s)
        elif response.status_code == 503:
            time.sleep(.500)
            # return response.status_code
