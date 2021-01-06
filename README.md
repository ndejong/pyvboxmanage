# PyVBoxManage
[![PyPi](https://img.shields.io/pypi/v/pyvboxmanage.svg)](https://pypi.python.org/pypi/pyvboxmanage/)
[![Python Versions](https://img.shields.io/pypi/pyversions/pyvboxmanage.svg)](https://github.com/ndejong/pyvboxmanage/)
[![Build Status](https://api.travis-ci.org/ndejong/pyvboxmanage.svg?branch=master)](https://travis-ci.org/ndejong/pyvboxmanage/)
[![Read the Docs](https://img.shields.io/readthedocs/pyvboxmanage)](https://pyvboxmanage.readthedocs.io)
![License](https://img.shields.io/github/license/ndejong/pyvboxmanage.svg)

PyVBoxManage is a wrapper tool around VBoxManage that facilitates the orchestration of VBoxManage commands from a
simple YAML configuration file that matches the input opts/args for VBoxManage.  This makes it possible to
implement common sequences of VBoxManage commands such as spinning up a new dev/test instance with different
hardware just by using a single command line with a configuration file.

Variables, output redirection, exit-triggers and returncode-exceptions are available to make flexible setups.

## Features
* Template variables
* Output redirection to STDOUT, STDERR, filename
* Exit triggers on string match within STDOUT or STDERR content (useful to prevent cloning/clobbering instance that is already running )
* Permit exit returncodes other than 0 in cases where they may occur (eg configuring a `--delete` action when the instance does not yet exist) 
* Dry mode to test configurations before running them
* Manage timeouts to prevent excessively long running VBoxManage commands (default 120 seconds, useful to prevent stalled VBoxManage tasks)
* Variable overrides through command line args are possible
* Documentation https://pyvboxmanage.readthedocs.io

## Installation
```shell
user@computer:~$ pip install pyvboxmanage
```

## Command Line Usage
Run a pyvboxmanage example configuration with `--verbose` logging output and override the variable 
`target_vmname` with a new value using the `--setting` argument.
```shell
user@computer:~$ pyvboxmanage --verbose examples/example01.yml --setting target_vmname=MyNewName  
DEBUG - pyvboxmanage v0.4.0
DEBUG - Loaded configuration file examples/example01.yml
DEBUG - Dry mode VBoxManage binary set to vboxmanage
DEBUG - Rendered command line: vboxmanage showvminfo MyNewName
DEBUG - Command line exec timeout 120
INFO - Successfully executed command line "vboxmanage showvminfo MyNewName"
DEBUG - Trigger string "running" is not present
DEBUG - Rendered command line: vboxmanage unregistervm MyNewName --delete
DEBUG - Command line exec timeout 120
INFO - Successfully executed command line "vboxmanage unregistervm MyNewName --delete"
DEBUG - Rendered command line: vboxmanage clonevm Ubuntu-20.04-master --basefolder "/opt/virtual-machines" --groups "/cicd" --mode "machine" --name "MyNewName" --register
DEBUG - Command line exec timeout 180
INFO - Successfully executed command line "vboxmanage clonevm Ubuntu-20.04-master --basefolder "/opt/virtual-machines" --groups "/cicd" --mode "machine" --name "MyNewName" --register"
DEBUG - Rendered command line: vboxmanage modifyvm MyNewName --bridgeadapter1 "enp0s25" --bridgeadapter2 "enp0s25" --bridgeadapter3 "enp0s25" --bridgeadapter4 "enp0s25" --cableconnected1 "on" --cableconnected2 "on" --cableconnected3 "on" --cableconnected4 "on" --macaddress1 "08002722E901" --macaddress2 "08002722E902" --macaddress3 "08002722E903" --macaddress4 "08002722E904" --nic1 "bridged" --nic2 "bridged" --nic3 "bridged" --nic4 "bridged" --nictype1 "82543GC" --nictype2 "82543GC" --nictype3 "82543GC" --nictype4 "82543GC"
DEBUG - Command line exec timeout 120
INFO - Successfully executed command line "vboxmanage modifyvm MyNewName --bridgeadapter1 "enp0s25" --bridgeadapter2 "enp0s25" --bridgeadapter3 "enp0s25" --bridgeadapter4 "enp0s25" --cableconnected1 "on" --cableconnected2 "on" --cableconnected3 "on" --cableconnected4 "on" --macaddress1 "08002722E901" --macaddress2 "08002722E902" --macaddress3 "08002722E903" --macaddress4 "08002722E904" --nic1 "bridged" --nic2 "bridged" --nic3 "bridged" --nic4 "bridged" --nictype1 "82543GC" --nictype2 "82543GC" --nictype3 "82543GC" --nictype4 "82543GC""
DEBUG - Rendered command line: vboxmanage startvm MyNewName --type "gui"
DEBUG - Command line exec timeout 120
INFO - Successfully executed command line "vboxmanage startvm MyNewName --type "gui""
```

Plenty more configuration examples [available here](https://pyvboxmanage.readthedocs.io/en/latest/docs/configuration-examples/).

## Project
* Github - [github.com/ndejong/pyvboxmanage](https://github.com/ndejong/pyvboxmanage)
* PyPI - [pypi.python.org/pypi/pyvboxmanage](https://pypi.python.org/pypi/pyvboxmanage/)
* TravisCI - [travis-ci.org/github/ndejong/pyvboxmanage](https://travis-ci.org/github/ndejong/pyvboxmanage)
* ReadTheDocs - [pyvboxmanage.readthedocs.io](https://pyvboxmanage.readthedocs.io)

---
Copyright &copy; 2020 Nicholas de Jong
