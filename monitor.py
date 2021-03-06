import data_picker
import setting
import alert_sender
import threading
import logger
import time
import sys
import os

class PSysMonitor(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        config = setting.monitor_config()
        self.server_name = config['server_name']
        self.admin_email = config['admin_email']
        self.last_heart_beat_date = ""
        self.picker = {}
        self.picker['cpu'] = data_picker.CpuDataPicker()
        self.picker['memory'] = data_picker.MemoryDataPicker()
        self.picker['network_send'] = data_picker.NetworkDataPicker(1)
        self.picker['network_receive'] = data_picker.NetworkDataPicker(2)
        _monitor_process_list =  config['process_list']# List of process to check exist
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

    def check_heartbeat(self):
        cur_date = time.strftime("%d/%m/%Y")
        if self.last_heart_beat_date != cur_date:
            self.last_heart_beat_date = cur_date
            title = "%s heart beat" % self.server_name
            message = "This is the heart beat from your dear server."
            if not alert_sender.send_mail(self.admin_email, title, message):
                logger.log("ERROR", "[PSysMonitor] Sending heartbeat mail error!")


    def run(self):
        logger.log("INFO", "[PSysMonitor] Engine Start!")
        for key, picker in self.picker.iteritems():
            picker.start()
        self.cur_system_status = False
        while(True):
            self.check_heartbeat()
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



