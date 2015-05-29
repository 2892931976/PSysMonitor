PSysMonitor
=================================================

##Introduce

This is a simple monitor for linux server, with the ability to check the usage of CPU, memory, network I/O and process existance.

##Base Tools

Python 2.\*
psutil

##Install

apt-get install pip
apt-get install python-dev
pip install psutil

then just clone this repo and you are ready to go

##Usage

You should change the setting in setting.py.

* The Email setting which will be used when PSysMonitor find something wrong
* The log file which you can get all record for each check
* The process you want to keep existance

After that, here we go:

<code>python monitor.py &</code>

And the monitor will run on background and record all logging message into log file, sending system message to  the admin's mailbox

##License

GNU GPL, of course~




