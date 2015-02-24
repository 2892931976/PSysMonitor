import data_picker
import alert_sender
import time

class Monitor():
    def __init__(self):
        self.data_picker = data_picker.DataPicker()
        self.conf = {}
        self.conf['interval'] = 10
        self.conf['cpu'] = 75 # If cpu percentage larger than 75, alert
        self.conf['memory'] = 80 # Memory usage percentage
        self.conf['network_speed'] = 1500 # Network speed in KB
        self.conf['process'] = (
                'ssserver',
                'tor',
                'nginx'
                ) # List of process to check exist

    def cpu_monitor(self):
        if self.conf['cpu'] < self.data_picker.get_cpu_percent():
            return '[CPU]Usage percentage higher than alert value!'
        return ''

    def run(self):
        while(True):
            message_body = self.cpu_monitor()
            if len(message_body)>0:
                alert_sender.send_alert(message_body)
            else:
                alert_sender.send_alert("System OK!")
            time.sleep(self.conf['interval'])

def main():
    monitor = Monitor()
    monitor.run()

if __name__ == '__main__':
    main()



