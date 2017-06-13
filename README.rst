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

Access methods
--------------

* configure : store configuration in ini file

| pyoxeconfgen_cli configure --host='10.100.8.10' --login='mtcl' --password='mtcl'


* connect :

| pyoxeconfgen_cli connect --host 'oxe02wbm.rainbow.tech-systems.fr' --login 'mtcl' --password 'mtcl'
| pyoxeconfgen_cli connect --ini


* logout :

| pyoxeconfgen_cli logout



Users methods
-------------

* create users

| pyoxeconfgen_cli createUsers --rangeSize=100 --rangeStart=8000 --setType "SIP_Extension"
| pyoxeconfgen_cli createUsers --rangeSize=10 --rangeStart=6000 --setType "UA_VIRTUAL"


* delete users

| pyoxeconfgen_cli deleteUsers --rangeSize=100 --rangeStart=8000



Licensing methods
-----------------

* set external flex server

| pyoxeconfgen_cli setFlexServer --ip 10.100.8.3
| pyoxeconfgen_cli setFlexServer --ip 10.100.8.3 --reboot



JSON model management
---------------------

* get OXE JSON data model

| pyoxeconfgen_cli getJsonModel --ip 10.100.8.10



Collect Information
-------------------

* get OXE Version

| pyoxeconfgen_cli getOxeVersion --ip 10.100.8.10



Rainbow connection methods
--------------------------

* get rainbow agent version running on OXE

| pyoxeconfgen_cli getRainbowAgentVersion --ip 10.100.8.10


* set Rainbow connection

| pyoxeconfgen_cli setRainbowConnection --rainbowDomain 'alexantr-all-in-one-dev-1.opentouch.cloud' --pbxId 'PBXd513-58ac-2d51-4737-a3a8-6b1e-6926-9e14' --activationCode 4567 --phoneBook Yes
| pyoxeconfgen_cli setRainbowConnection --ini


* update ccca.cfg for rainbow test environment ALL-IN-ONE

| pyoxeconfgen_cli updateCccaCfg --ip 10.100.8.14 --port 22 --login mtcl --password mtcl --apiserver alexantr-agent.openrainbow.org



OMS configuration methods
-------------------------

* Set main Call Server & cristal number to auto-discovery

| pyoxeconfgen_cli setFlexServer --ip 10.100.8.3



Shelves methods
---------------

* Create shelf

* Update ethernet parameters


SIP management
--------------

* Default configuration to enable SIP (default trunk groups + SIP GW + SIP Proxy)


Netadmin management
-------------------


Swinst management
-----------------



Development
===========

To run the all tests run ::

    py.test

