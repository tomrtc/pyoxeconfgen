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
import json
import datetime

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


@cli.command('configure')
@click.option('--host', help='OXE IP address / FQDN')
@click.option('--login', help='OXE login', default='mtcl')
@click.option('--password', help='OXE password', default='mtcl')
@click.option('--proxies', help='API server FQDN', default=None)
def cli_configure(**kwargs):
    oxe_ip = kwargs.get('host', None)
    if oxe_ip is None:
        print('--host option is mandatory')
        exit()
    login = kwargs.get('login', 'mtcl')
    password = kwargs.get('password', 'mtcl')
    proxies = kwargs.get('proxies', None)
    configure(oxe_ip, login, password, proxies)


@cli.command('connect')
@click.option('--host', help='OXE IP address / FQDN')
@click.option('--login', help='OXE login', default='mtcl')
@click.option('--password', help='OXE password', default='mtcl')
@click.option('--proxies', help='API server FQDN', default=None)
def cli_connect(**kwargs):
    host = kwargs.get('host', None)
    if host is None:
        print('--host option is mandatory')
        exit()
    login = kwargs.get('login', 'mtcl')
    password = kwargs.get('password', 'mtcl')
    proxies = kwargs.get('proxies', None)
    oxe_authenticate(host, login, password, proxies)


@cli.command('logout')
def cli_logout():
    token, host = get_auth_from_cache()
    oxe_logout(host, token)


@cli.command('getJsonModel')
def cli_get_json_model():
    token, host = get_auth_from_cache()
    json_model = json.loads(oxe_get_json_model(host, token))
    horodating = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    with open('/tmp/OXE_' + host + '_' + horodating + '.json', 'w') as fh:
        fh.write(json.dumps(json_model, indent=4, sort_keys=True))


@cli.command('createUsers')
@click.option('--rangeSize', help='range of users to create', default=1)
@click.option('--rangeStart', help='first internal number', default=8000)
@click.option('--setType', help='set type')
def cli_create_users(**kwargs):
    range_size = int(kwargs.get('rangesize', 1))
    range_start = int(kwargs.get('rangestart', 8000))
    set_type = kwargs.get('settype', 'SIP_Extension')
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    token, host = get_auth_from_cache()
    bar = progressbar.ProgressBar()
    # json_model['definitions']['Station_Type']['values'] # to control set type with OXE dictionary
    for extension_number in bar(range(range_start, range_start + range_size)):
        oxe_create_user(host, token, extension_number, set_type + str(extension_number), extension_number, set_type, 10)


@cli.command('deleteUsers')
@click.option('--rangeSize', help='range of users to create', default=1)
@click.option('--rangeStart', help='first internal number', default=8000)
def cli_delete_users(**kwargs):
    range_size = int(kwargs.get('rangesize', 1))
    range_start = int(kwargs.get('rangestart', 8000))
    token, host = get_auth_from_cache()
    bar = progressbar.ProgressBar()
    for extension_number in bar(range(range_start, range_start + range_size)):
        oxe_delete_user(host, token, extension_number, 10)


@cli.command('setFlexServer')
@click.option('--ip', help='External Flex server IP address')
@click.option('--port', help='External Flex port', default=27000)
def cli_set_flex_server(**kwargs):
    flex_ip_address = kwargs.get('ip', None)
    if flex_ip_address is None:
        print('--flexIp option is mandatory. Exiting ...')
        exit()
    flex_port = kwargs.get('port', 27000)
    token, host = get_auth_from_cache()
    oxe_set_flex(host, token, flex_ip_address, flex_port)
    print('WARNING: OXE must be rebooted')


@cli.command('setRainbowConnection')
@click.option('--rainbowDomain', help='Rainbow Domain')
@click.option('--rainbowId', help='PBX Rainbow ID')
@click.option('--phoneBook', help='', default='YES')
@click.option('--activationCode', help='PBX activation code')
def cli_set_rainbow_connection(**kwargs):
    rainbow_domain = kwargs.get('rainbowDomain', None)
    if rainbow_domain is None:
        print('--rainbowDomain option is mandatory. Exiting ...')
        exit()
    rainbow_id = kwargs.get('rainbowId', None)
    if rainbow_id is None:
        print('--rainbowId option is mandatory. Exiting ...')
        exit()
    # phone_book = kwargs.get('phoneBook', YES)
    activation_code = kwargs.get('activationCode', None)
    if activation_code is None:
        print('--activationCode option is mandatory. Exiting ...')
        exit()

# Create entity
# Create Shelves/OMS
# Set SIP GW/Pxy/Reg
# Create SIP Ext GW
# Create VAA
# Create Attendant
# Create Hunt Group
# Create 4645
# Add mevo to users
# Add call by name to users


@cli.command('getRainbowAgentVersion')
@click.option('--ip', help='OXE IP address')
@click.option('--port', help='OXE SSH port', default=22)
@click.option('--login', help='user login', default='mtcl')
@click.option('--password', help='user password', default='mtcl')
def cli_get_rainbow_agent_version(**kwargs):
    ip = kwargs.get('ip')
    if ip is None:
        print('--ip option is mandatory. Exiting ...')
        exit()
    port = kwargs.get('port')
    login = kwargs.get('login')
    password = kwargs.get('password')
    oxe_get_rainbow_agent_version(ip, port, login, password)


@cli.command('getOxeVersion')
@click.option('--ip', help='OXE IP address')
@click.option('--port', help='OXE SSH port', default=22)
@click.option('--login', help='user login', default='mtcl')
@click.option('--password', help='user password', default='mtcl')
def cli_get_rainbow_agent_version(**kwargs):
    ip = kwargs.get('ip')
    if ip is None:
        print('--ip option is mandatory. Exiting ...')
        exit()
    port = kwargs.get('port')
    login = kwargs.get('login')
    password = kwargs.get('password')
    oxe_get_oxe_version(ip, port, login, password)


@cli.command('updateCccaCfg')
@click.option('--ip', help='OXE IP address')
@click.option('--port', help='OXE SSH port', default=22)
@click.option('--login', help='user login', default='mtcl')
@click.option('--password', help='user password', default='mtcl')
@click.option('--apiserver', help='API server FQDN')
def cli_get_rainbow_agent_version(**kwargs):
    ip = kwargs.get('ip')
    if ip is None:
        print('--ip option is mandatory. Exiting ...')
        exit()
    api_server = kwargs.get('apiserver')
    if ip is None:
        print('--api_server option is mandatory. Exiting ...')
        exit()
    port = kwargs.get('port')
    login = kwargs.get('login')
    password = kwargs.get('password')
    oxe_update_ccca_cfg(ip, port, login, password, api_server)
