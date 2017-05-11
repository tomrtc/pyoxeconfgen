#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# Here go you application specific code.

import click
from pyoxeconfgen.__init__ import __version__
from clickclick import AliasedGroup
from pyoxeconfgen.oxeconfig import *
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import progressbar
import pprint
import json

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

STYLES = {
    'FINE': {'fg': 'green'},
    'ERROR': {'fg': 'red'},
    'WARNING': {'fg': 'yellow', 'bold': True},
}

TITLES = {
    'state': 'Status',
    'creation_time': 'Creation Date',
    'id': 'Identifier',
    'desc': 'Description',
    'name': 'Name',
}

MAX_COLUMN_WIDTHS = {
    'desc': 50,
    'name': 20,
}


# Version
def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo('confgen version: {}'.format(__version__))
    ctx.exit()


# CLI
@click.group(cls=AliasedGroup, context_settings=CONTEXT_SETTINGS)
@click.option('-V', '--version', is_flag=True, callback=print_version, expose_value=False, is_eager=True,
              help='Print the current version number and exit.')
def cli():
    pass


@cli.command('createUsers')
@click.option('--oxeIp', help='OXE CS IP@')
@click.option('--oxeLogin', help='OXE login', default='mtcl')
@click.option('--oxePassword', help='OXE password', default='mtcl')
@click.option('--rangeSize', help='range of users to create', default=100)
@click.option('--rangeStart', help='first internal number')
@click.option('--setType', help='set type')
def cli_create_users(**kwargs):
    ip_address = kwargs.get('oxeip', None)
    # for i, j in kwargs.items():
    #     print('DEBUG_1: {} : {}', iact_cd, j)
    # print('DEBUG_2: {} ', ip_address)
    if ip_address is None:
        print('--oxeIp option is mandatory. Exiting ...')
        exit()
    oxe_login = kwargs.get('oxelogin')
    oxe_password = kwargs.get('oxepassword')
    range_size = int(kwargs.get('rangesize'))
    range_start = int(kwargs.get('rangestart', 0))
    if range_start is None:
        print('--rangeStart option is mandatory. Exiting ...')
        exit()
    set_type = kwargs.get('settype', 'SIP_Extension')
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    token = oxe_authenticate(ip_address, oxe_login, oxe_password)
    header_post = {
        'Authorization': 'Bearer ' + token,
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    bar = progressbar.ProgressBar()
    for extensionNumber in bar(range(range_start, range_start + range_size)):
        oxe_create_user(ip_address, extensionNumber, 'SIP', extensionNumber, set_type, header_post)


# deleteUsers


@cli.command('setRainbowConnection')
@click.option('--rainbowDomain', help='Rainbow Domain')
@click.option('--rainbowId', help='PBX Rainbow ID')
@click.option('--phoneBook', help='', default='YES')
@click.option('--activationCode', help='PBX activation code')
def set_rainbow_connection(**kwargs):
    rainbow_domain = kwargs.get('rainbowDomain', None)
    if rainbow_domain is None:
        print('--rainbowDomain option is mandatory. Exiting ...')
        exit()
    rainbow_id = kwargs.get('rainbowId', None)
    if rainbow_id is None:
        print('--rainbowId option is mandatory. Exiting ...')
        exit()
    phone_book = kwargs.get('phoneBook', YES)
    activation_code = kwargs.get('activationCode', None)
    if activation_code is None:
        print('--activationCode option is mandatory. Exiting ...')
        exit()

# Create entity
# Set Flex Server
# Create Shelves/OMS
# Set SIP GW/Pxy/Reg
# Create SIP Ext GW
# Create VAA
# Create Attendant
# Create Hunt Group
# Create 4645
