PSysMonitor
=================================================

##Introduce

This is a simple monitor for linux server, with the ability to check the usage of CPU, memory, network I/O and process existance.

##Base Tools

Python 2.\*
psutil

##Third Party Service

[Bellringer](http://tonggao.baidu.com)

##Usage

Firstly you should install the python, and psutil.
Secondly you can register an account on Bellringer.
Thirdly, clone this repo, and change the config inside code.(monitor.py and alert\_sender.py):

* The process you want to keep existance
* The threshold of each system resources
* The API key and ID for bellringer

After that, here we go:

<code>python monitor.py &</code>

And the monitor will run on background and record all logging message into trace.log, sending system message to bellringer.

##License

GNU GPL, of course~




