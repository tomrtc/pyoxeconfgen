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

# CLI handlfrom confgen.otecConfig import *ing
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
def createUsers(**kwargs):
    ipAddr = kwargs.get('oxeip', None)
    for i, j in kwargs.items():
        print('DEBUG_1: {} : {}', i, j)
    print ('DEBUG_2: {} ', ipAddr)
    if ipAddr is None:
        print('--oxeIp option is mandatory. Exiting ...')
        exit()
    oxeLgn = kwargs.get('oxelogin')
    oxePwd = kwargs.get('oxepassword')
    rngSz = int(kwargs.get('rangesize'))
    rngSt = int(kwargs.get('rangestart', 0))
    if rngSt is None:
        print('--rangeStart option is mandatory. Exiting ...')
        exit()
    setTp = kwargs.get('settype', 'SIP_Extension')
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    token = authenticate(ipAddr, oxeLgn, oxePwd)
    headerPost = {'Authorization': 'Bearer ' + token,
                  'accept': 'application/json',
                  'Content-Type': 'application/json'}
    bar = progressbar.ProgressBar()
    for extensionNumber in bar(range(rngSt, rngSt + rngSz)):
        createUser(ipAddr, extensionNumber, 'SIP', extensionNumber, setTp, headerPost)


@cli.command('setRainbowConnection')
@click.option('--rainbowDomain', help='Rainbow Domain')
@click.option('--rainbowId', help='PBX Rainbow ID')
@click.option('--phoneBook', help='', default='YES')
@click.option('--activationCode', help='PBX activation code')
def setRainbowConnection(**kwargs):
    rbwdmn = kwargs.get('rainbowDomain', None)
    if rbwdmn is None:
        print('--rainbowDomain option is mandatory. Exiting ...')
        exit()
    rbwid == kwargs.get('rainbowId', None)
    if rbwId is None:
        print('--rainbowId option is mandatory. Exiting ...')
        exit()
    phnbk == kwargs.get('phoneBook', YES)
    actcd == kwargs.get('activationCode', None)
    if actcd is None:
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