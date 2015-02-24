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
            return '[CPU]Usage percentage higher than threshold!'
        return ''

    def memory_monitor(self):
        if self.conf['memory'] < self.data_picker.get_memory_used_percent():
            return '[MEMORY]Usage percentage higher than threshold!'
        return ''

    def network_monitor(self):
        message = ''
        speeds = self.data_picker.get_network_speed()
        if self.conf['network_speed'] < speeds['send']:
            message += '[NETWORK]Sending speed faster than threshold!'
        if self.conf['network_speed'] < speeds['receive']:
            message += '[NETWORK]Receiving speed faster than threshold!'
        return message

    def process_monitor(self):
        return ''

    def run(self):
        while(True):
            message_body = ""
            message_body += self.cpu_monitor()
            message_body += self.memory_monitor()
            message_body += self.network_monitor()
            message_body += self.process_monitor()

            if len(message_body)>0:
                alert_sender.send_alert(message_body)
            else:
                alert_sender.send_alert("System OK!")
            print message_body

            time.sleep(self.conf['interval'])

def main():
    monitor = Monitor()
    monitor.run()

if __name__ == '__main__':
    main()



