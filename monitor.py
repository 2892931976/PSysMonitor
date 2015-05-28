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
        self.server_name = "My Server"
        self.admin_email = "mybuffer@163.com"
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
                'fteproxy.bin',
                'notfound'
                ) # List of process to check exist
        self.picker['process'] = data_picker.ProcessPicker(_monitor_process_list)
        self.conf = {}
        self.conf['interval'] = 10
        self.conf['cpu'] = 75 # If cpu percentage larger than 75, alert
        self.conf['memory'] = 80 # Memory usage percentage
        self.conf['network_send'] = 1200 # Network speed in KB
        self.conf['network_receive'] = 1200 # Network speed in KB
        self.conf['process'] = 0 # When process monitor status is 1, it means something wrong

    def check_values(self):
        logger.log("INFO", "[PSysMonitor] Begin to refresh status")
        alert_message = ""
        for key, picker in self.picker.iteritems():
            picker_data = picker.fetch_data()
            message = picker.fetch_describe()
            if self.conf[key] < picker_data['value']:
                logger.log("WARNING", message)
                alert_message += message
            else:
                logger.log("INFO", message)
        return alert_message

    def report_exception(self, message):
        if not alert_sender.send_mail(self.admin_email, self.server_name+" System Warning", message):
            logger.log("ERROR", "[PSysMonitor] Sending mail error!")

    def report_ok(self):
        if not alert_sender.send_mail(self.admin_email, self.server_name+" System Recover", "Congratulation"):
            logger.log("ERROR", "[PSysMonitor] Sending mail error!")

    def run(self):
        logger.log("INFO", "[PSysMonitor] Engine Start!")
        for key, picker in self.picker.iteritems():
            picker.start()
        self.cur_system_status = False
        while(True):
            time.sleep(self.conf['interval'])
            alert_message = self.check_values()
            if len(alert_message) > 0:
                if not self.cur_system_status:
                    self.cur_system_status = True
                    self.report_exception(alert_message)
            elif self.cur_system_status:
                self.cur_system_status = False
                self.report_ok()

def main():
    monitor = PSysMonitor()
    try:
        monitor.start()
    except:
        logger.log("ERROR", sys.exc_info()[0])
        raise

if __name__ == '__main__':
    main()



