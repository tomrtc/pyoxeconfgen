===========
Pyoxeconfgen
===========

Automation tool managing ALE OmniPCX Enterprise configuration. This tools is using OXE REST API (only available from version M1.403)

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

pyoxeconfgen_cli createUsers --oxeIp="10.100.8.10" --oxePassword='Pcloud123!' --rangeSize=100 --rangeStart=8000 --setType "SIP_Extension"
pyoxeconfgen_cli createUsers --oxeIp="10.100.8.10" --oxePassword='Pcloud123!' --rangeSize=100 --rangeStart=8000 --setType "UA_VIRTUAL"

Development
===========

To run the all tests run ::

    py.test

