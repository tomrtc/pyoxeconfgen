""" OXE connection methods """
import configparser
import pprint
import requests
import requests.packages
import sys
import os
import json
from pyoxeconfgen.oxe_access import oxe_set_headers


# create default trunk groups
def oxe_create_sip_default_trunk_groups(host, token, trunk_id):
    payload = {
        'Homo_Net_For_Direct_RTP': 'Yes',
        'Number_Of_Digits_To_Send': '4',
        'Public_Network_Category_Id': '31',
        'Remote_Network': '14',
        'Signalization_Variation': 'ABC_F_VARIANT',
        'T2_Specificity': 'SIP',
        'Trunk_Group_Name': 'SIP'
    }
    creation = requests.post('https://' + host + '/api/mgt/1.0/Node/1/Trunk_Group_Overview/' + trunk_id,
                             json=payload,
                             headers=oxe_set_headers(token, 'POST'),
                             verify=False)
    pprint.pprint(creation.json())


# configure sip gateway
def oxe_sip_gateway(host, token):
    payload = {'SIP_Subnetwork': '14', 'SIP_Trunk_Group': '14'}
    modification = requests.put('https://' + host + '/api/mgt/1.0/Node/1/SIP/1/SIP_Gateway/1',
                                json=payload,
                                headers=oxe_set_headers(token, 'PUT'),
                                verify=False)
    pprint.pprint(modification.json())


# configure sip proxy
def oxe_sip_proxy(host, token):
    payload = {'SIP_min_auth_method': 'SIP_None', 'SIP_Move_To_TCP': 'false', 'ReTransNo_Invite': '4'}
    modification = requests.put('https://' + host + '/api/mgt/1.0/Node/1/SIP/1/SIP_Proxy/1',
                                json=payload,
                                headers=oxe_set_headers(token, 'PUT'),
                                verify=False)
    pprint.pprint(modification.json())
