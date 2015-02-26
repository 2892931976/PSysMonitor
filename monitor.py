import data_picker
import alert_sender
import logger
import time
import sys
import os

class Monitor():
    def __init__(self):
        self.data_picker = data_picker.DataPicker()
        self.conf = {}
        self.conf['interval'] = 10
        self.conf['cpu'] = 75 # If cpu percentage larger than 75, alert
        self.conf['memory'] = 80 # Memory usage percentage
        self.conf['network_speed'] = 1200 # Network speed in KB
        self.conf['process'] = (
                'ssserver',
                'tor',
                'nginx',
                'php5-fpm',
                'fteproxy.bin'
                ) # List of process to check exist
    def threshold_monitor(self, type_str, threshold, current_value):
        if threshold < current_value:
            return '[%s] %d higher than threshold!' % (type_str, current_value)
        return ''

    def cpu_monitor(self):
        current_usage = self.data_picker.get_cpu_percent()
        return self.threshold_monitor('CPU_PERCENTAGE', self.conf['cpu'], current_usage)

    def memory_monitor(self):
        current_usage =  self.data_picker.get_memory_used_percent()
        return self.threshold_monitor('MEMORY_PERCENTAGE', self.conf['memory'], current_usage)

    def network_monitor(self):
        message = ''
        speeds = self.data_picker.get_network_speed()
        message += self.threshold_monitor('NETWORK_SEND', self.conf['network_speed'], speeds['send'])
        message += self.threshold_monitor('NETWORK_RECEIVE', self.conf['network_speed'], speeds['receive'])
        return message

    def process_monitor(self):
        not_found_list = ''
        process_list = self.data_picker.get_process_list()
        for p in self.conf['process']:
            if p not in process_list:
                not_found_list += p+' '
        if len(not_found_list) > 0:
            return '[PROCESS]Not found: '+not_found_list
        return ''

    def run(self):
        while(True):
            message_body = ""
            message_body += self.cpu_monitor()
            message_body += self.memory_monitor()
            message_body += self.network_monitor()
            message_body += self.process_monitor()

            if len(message_body)==0:
                message_body = 'System OK'
            else:
                logger.log("WARNING", message_body)
            try:
                alert_sender.send_alert(message_body)
            except Exception as ex:
                logger.log("ERROR", 'Alert sending error:'+str(ex))

            time.sleep(self.conf['interval'])

def main():
    monitor = Monitor()
    try:
        monitor.run()
    except:
        logger.log("ERROR", sys.exc_info()[0])
        raise

if __name__ == '__main__':
    main()



