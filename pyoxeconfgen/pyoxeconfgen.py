#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# Here go you application specific code.

import click
import progressbar
import datetime
import json
import requests
from clickclick import AliasedGroup
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from pyoxeconfgen.__init__ import __version__
from pyoxeconfgen.oxe_commands import *
from pyoxeconfgen.oxe_access import oxe_get_auth_from_cache
from pyoxeconfgen.oxe_access import oxe_logout
from pyoxeconfgen.oxe_access import oxe_configure
from pyoxeconfgen.oxe_access import oxe_get_config
from pyoxeconfgen.oxe_access import oxe_authenticate
from pyoxeconfgen.oxe_info import *
from pyoxeconfgen.oxe_users import *
from pyoxeconfgen.oxe_rainbow import *
from pyoxeconfgen.oxe_licensing import *


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
@click.option('--password', help='mtcl password', default='mtcl')
@click.option('--proxies', help='API server FQDN', default=None)
def cli_configure(**kwargs):
    oxe_ip = kwargs.get('host', None)
    if oxe_ip is None:
        print('--host option is mandatory')
        exit()
    password = kwargs.get('password', 'mtcl')
    proxies = kwargs.get('proxies', None)
    oxe_configure(oxe_ip, 'mtcl', password, proxies)


@cli.command('connect')
@click.option('--host', help='OXE IP address / FQDN')
@click.option('--password', help='mtcl password', default='mtcl')
@click.option('--proxies', help='API server FQDN', default=None)
@click.option('--ini', help='Config File', is_flag=True)
def cli_connect(**kwargs):
    ini = kwargs.get('ini', False)
    if ini is False:
        host = kwargs.get('host', None)
        if host is None:
            print('--host option is mandatory')
            exit()
        password = kwargs.get('password', 'mtcl')
        proxies = kwargs.get('proxies', None)
    else:
        host, login, password, proxies = oxe_get_config()
    oxe_authenticate(host, 'mtcl', password, proxies)


@cli.command('logout')
def cli_logout():
    token, host = oxe_get_auth_from_cache()
    oxe_logout(host, token)


@cli.command('getJsonModel')
def cli_get_json_model():
    token, host = oxe_get_auth_from_cache()
    json_model = json.loads(oxe_get_json_model(host, token))
    horodating = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    with open('/tmp/OXE_' + host + '_' + horodating + '.json', 'w') as fh:
        fh.write(json.dumps(json_model, indent=4, sort_keys=True))


@cli.command('createUsers')
@click.option('--rangeSize', help='range of users to create', default=1)
@click.option('--rangeStart', help='first internal number', default=8000)
@click.option('--setType', help='set type', default='SIP_Extension')
@click.option('--companyId', help='Company Index', default=1)
def cli_create_users(**kwargs):
    range_size = int(kwargs.get('rangesize', 1))
    range_start = int(kwargs.get('rangestart', 8000))
    set_type = kwargs.get('settype', 'SIP_Extension')
    company_id = kwargs.get('companyid', 1)
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    token, host = oxe_get_auth_from_cache()
    bar = progressbar.ProgressBar()
    # json_model['definitions']['Station_Type']['values'] # to control set type with OXE dictionary
    for extension_number in bar(range(range_start, range_start + range_size)):
        if company_id < 10:
            last_name = 'LC0' + str(company_id) + 'U' + str(extension_number)
            first_name = 'FC0' + str(company_id) + 'U' + str(extension_number)
        else:
            last_name = 'LC0' + str(company_id) + 'U' + str(extension_number)
            first_name = 'FC0' + str(company_id) + 'U' + str(extension_number)
        oxe_create_user(host, token, extension_number, last_name, first_name, set_type, 10)


@cli.command('deleteUsers')
@click.option('--rangeSize', help='range of users to create', default=1)
@click.option('--rangeStart', help='first internal number', default=8000)
def cli_delete_users(**kwargs):
    range_size = int(kwargs.get('rangesize', 1))
    range_start = int(kwargs.get('rangestart', 8000))
    token, host = oxe_get_auth_from_cache()
    bar = progressbar.ProgressBar()
    for extension_number in bar(range(range_start, range_start + range_size)):
        oxe_delete_user(host, token, extension_number, 10)


@cli.command('setFlexServer')
@click.option('--ip', help='External Flex server IP address')
@click.option('--port', help='External Flex port', default=27000)
def cli_set_flex_server(**kwargs):
    flex_ip_address = kwargs.get('ip', None)
    if flex_ip_address is None:
        print('--ip option is mandatory. Exiting ...')
        exit()
    flex_port = kwargs.get('port', 27000)
    token, host = oxe_get_auth_from_cache()
    oxe_set_flex(host, token, flex_ip_address, flex_port)
    print('WARNING: OXE must be rebooted')


@cli.command('setRainbowConnection')
@click.option('--rainbowDomain', help='Rainbow Domain')
@click.option('--pbxId', help='PBX Rainbow ID')
@click.option('--phoneBook', help='Send OXE phone book to Rainbow', default='Yes')
@click.option('--activationCode', help='PBX activation code')
@click.option('--ini', help='config file use', is_flag=True)
def cli_set_rainbow_connection(**kwargs):
    token, host = oxe_get_auth_from_cache()
    if kwargs.get('ini') is False:
        rainbow_domain = kwargs.get('rainbowdomain', None)
        if rainbow_domain is None:
            print('--rainbowDomain option is mandatory. Exiting ...')
            exit()
        pbx_id = kwargs.get('pbxid', None)
        if pbx_id is None:
            print('--pbxId option is mandatory. Exiting ...')
            exit()
        phone_book = kwargs.get('phonebook', 'Yes')
        activation_code = kwargs.get('activationcode', None)
        if activation_code is None:
            print('--activationCode option is mandatory. Exiting ...')
            exit()
    else:
        rainbow_domain, pbx_id, activation_code, rainbow_host = oxe_get_rainbow_config()
        phone_book = 'Yes'
    oxe_set_rainbow(host, token, rainbow_domain, pbx_id, activation_code, phone_book)


@cli.command('enableSIP')
@click.option('--ip', help='OXE IP address')
def cli_enable_sip(**kwargs):
    print('todo')


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
@click.option('--password', help='mtcl password', default='mtcl')
def cli_get_rainbow_agent_version(**kwargs):
    ip = kwargs.get('ip')
    if ip is None:
        print('--ip option is mandatory. Exiting ...')
        exit()
    port = kwargs.get('port')
    password = kwargs.get('password')
    oxe_get_rainbow_agent_version(ip, port, 'mtcl', password)


@cli.command('getOxeVersion')
@click.option('--ip', help='OXE IP address')
@click.option('--port', help='OXE SSH port', default=22)
@click.option('--login', help='mtcl login', default='mtcl')
@click.option('--password', help='mtcl password', default='mtcl')
def cli_get_rainbow_agent_version(**kwargs):
    ip = kwargs.get('ip')
    if ip is None:
        print('--ip option is mandatory. Exiting ...')
        exit()
    port = kwargs.get('port')
    login = kwargs.get('login')
    password = kwargs.get('password')
    oxe_get_oxe_version(ip, port, login, password)


@cli.command('oxeReboot')
@click.option('--ip', help='OXE IP address')
@click.option('--port', help='OXE SSH port', default=22)
@click.option('--password', help='mtcl password', default='mtcl')
@click.option('--swinstPassword', help='swinst password', default='SoftInst')
def cli_get_rainbow_agent_version(**kwargs):
    ip = kwargs.get('ip')
    if ip is None:
        print('--ip option is mandatory. Exiting ...')
        exit()
    port = kwargs.get('port')
    password = kwargs.get('password')
    swinst_password = kwargs.get('swinstpassword')
    oxe_reboot(ip, port, 'mtcl', password, swinst_password)


@cli.command('updateCccaCfg')
@click.option('--ip', help='OXE IP address')
@click.option('--port', help='OXE SSH port', default=22)
@click.option('--password', help='mtcl password', default='mtcl')
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
    password = kwargs.get('password')
    oxe_update_ccca_cfg_dev_all_in_one(ip, port, 'mtcl', password, api_server)
