============
Pyoxeconfgen
============

Automation tool managing ALE OmniPCX Enterprise configuration. This tools is using OXE REST API (only available for OXE version >= M1.403.10)

Installation
============

::

    pip install git+https://github.com/alexandretrentesaux/pyoxeconfgen#egg=pyoxeconfgen

Or in a develop mode after downloading a zip or cloning the git repository ::

    git clone https://github.com/alexandretrentesaux/pyoxeconfgen
    cd pyoxeconfgen
    pip install -e .

Or in a develop mode from a git repository ::

    pip install -e git+https://github.com/alexandretrentesaux/pyoxeconfgen#egg=pyoxeconfgen

Once installed you can run ::

 pyoxeconfgen_cli --help

Examples
========

* configure : store configuration in ini file

pyoxeconfgen_cli configure --host='10.100.8.10' --login='mtcl' --password='mtcl'

* connect :

pyoxeconfgen_cli connect --host 'oxe02wbm.rainbow.tech-systems.fr' --login 'mtcl' --password 'mtcl'

* logout :

pyoxeconfgen_cli logout

* create users

pyoxeconfgen_cli createUsers --rangeSize=100 --rangeStart=8000 --setType "SIP_Extension"
pyoxeconfgen_cli createUsers --rangeSize=10 --rangeStart=6000 --setType "UA_VIRTUAL"

* delete users

pyoxeconfgen_cli deleteUsers --rangeSize=100 --rangeStart=8000

* set external flex server

pyoxeconfgen_cli setFlexServer --flexIp 10.100.8.3

* get OXE JSON data model

pyoxeconfgen_cli getJsonModel --oxeIp 10.100.8.11


Development
===========

To run the all tests run ::

    py.test

