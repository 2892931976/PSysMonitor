import data_picker
import alert_sender
import threading
import logger
import time
import sys
import os

class PSysMonitor(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.picker = {}
        self.picker['cpu'] = data_picker.CpuDataPicker()
        self.picker['memory'] = data_picker.MemoryDataPicker()
        self.picker['network_send'] = data_picker.NetworkDataPicker(1)
        self.picker['network_receive'] = data_picker.NetworkDataPicker(2)
        _monitor_process_list = (
                'ss-server',
                'tor',
                'nginx',
                'php5-fpm',
                'fteproxy.bin'
                ) # List of process to check exist
        self.picker['process'] = data_picker.ProcessPicker(_monitor_process_list)
        self.conf = {}
        self.conf['interval'] = 10
        self.conf['cpu'] = 75 # If cpu percentage larger than 75, alert
        self.conf['memory'] = 80 # Memory usage percentage
        self.conf['network_send'] = 1200 # Network speed in KB
        self.conf['network_receive'] = 1200 # Network speed in KB
        self.conf['process'] = 1 # When process monitor status is 1, it means something wrong

    def check_values(self):
        logger.log("INFO", "[PSysMonitor] Begin to refresh status")
        for key, picker in self.picker.iteritems():
            picker_data = picker.fetch_data()
            if self.conf[key] < picker_data['value']:
                logger.log("WARNING", "[%s][%s][%s]" % (picker_data['picker_name'], picker_data['value'], picker_data['message']))
            else:
                logger.log("INFO", "[%s][%s][%s]" % (picker_data['picker_name'], picker_data['value'], picker_data['message']))

    def run(self):
        logger.log("INFO", "[PSysMonitor] Engine Start!")
        for key, picker in self.picker.iteritems():
            picker.start()
        while(True):
            time.sleep(self.conf['interval'])
            self.check_values()


def main():
    monitor = PSysMonitor()
    try:
        monitor.start()
    except:
        logger.log("ERROR", sys.exc_info()[0])
        raise

if __name__ == '__main__':
    main()



