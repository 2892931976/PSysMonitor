import psutil
import threading
import time

class BasicDataPicker(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.time_interval = 1
        self.picker_name = 'basic picker'
        self.data_report = {
                'PickerName': self.picker_name,
                'value':0,
                'message':'Nothing yet.'
            }

    def run(self):
        print '[Info][Data Picker] Engine start:'+self.picker_name
        while True:
            self.pick()
            time.sleep(self.time_interval)

    def pick(self):
        print '[Warning][Data Picker] It\'s the basic picker so it just says anything ok.'
        self.data_report['value'] = 0
        self.data_report['message'] = "Everything ok. Believe me."

    def fetch_data(self):
        return self.data_report


class DataPicker():
    def get_cpu_percent(self):
        return psutil.cpu_percent(interval=1)

    def get_memory_used_percent(self):
        data = psutil.virtual_memory()
        return data[2]

    def get_network_speed(self):
        info_before = self._get_network_data_count()
        time.sleep(1)
        info_after = self._get_network_data_count()

        def cal_rate(after, before):
            return (after - before) / 1024.0 # byte to kB
        send_speed = cal_rate(info_after['send'], info_before['send'])
        receive_speed = cal_rate(info_after['receive'], info_before['receive'])

        return {'send':send_speed, 'receive':receive_speed}

    def _get_network_data_count(self):
        all_data = psutil.net_io_counters(True)
        eth_data = all_data['eth0']
        return {'send':eth_data[0], 'receive':eth_data[1]}

    def get_user_info(self):
        return psutil.users()

    def get_process_list(self):
        process_list = psutil.process_iter()
        process_name_list = []
        for process in process_list:
            process_name_list.append(process.name())
        return process_name_list

def main_test():
    basic_picker = BasicDataPicker()
    basic_picker.start()

if __name__ == '__main__':
    main_test()
