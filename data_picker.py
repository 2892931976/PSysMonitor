import psutil
import os
import threading
import time

class BasicDataPicker(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.time_interval = 1
        self.data_report = {
                'picker_name': 'basic picker',
                'value':0,
                'message':'Nothing yet.'
            }

    def run(self):
        while True:
            self.pick()
            time.sleep(self.time_interval)

    def pick(self):
        print '[Warning][Data Picker] It\'s the basic picker so it just says everything ok.'
        self.data_report['value'] = 0
        self.data_report['message'] = "Everything ok. Believe me."

    def fetch_data(self):
        return self.data_report

class CpuDataPicker(BasicDataPicker):
    def __init__(self):
        BasicDataPicker.__init__(self)
        self.data_report['picker_name'] = "CPU"

    def pick(self):
        self.data_report['value'] = psutil.cpu_percent(interval=1)
        self.data_report['message'] = 'refresh at: '+time.asctime()

class MemoryDataPicker(BasicDataPicker):
    def __init__(self):
        BasicDataPicker.__init__(self)
        self.data_report['picker_name'] = "Memory"

    def pick(self):
        data = psutil.virtual_memory()
        self.data_report['value'] = data[2]
        self.data_report['message'] = 'refresh at: '+time.asctime()

class NetworkDataPicker(BasicDataPicker):
    def __init__(self, _direction):
        BasicDataPicker.__init__(self)
        self.data_report['picker_name'] = "Network"
        if _direction == 1:
            self.direction = 'send'
        else:
            self.direction = 'receive'

    def _get_network_data_count(self):
        all_data = psutil.net_io_counters(True)
        eth_data = all_data['eth0']
        return {'send':eth_data[0], 'receive':eth_data[1]}

    def pick(self):
        info_before = self._get_network_data_count()
        time.sleep(1)
        info_after = self._get_network_data_count()

        def cal_rate(after, before):
            return (after - before) / 1024.0 # byte to kB
        self.data_report['value'] = cal_rate(info_after[self.direction], info_before[self.direction])
        self.data_report['message'] = 'Network speed(KB/s) for '+self.direction

class ProcessPicker(BasicDataPicker):
    def __init__(self, _process_list):
        BasicDataPicker.__init__(self)
        self.data_report['picker_name'] = "Process"
        self.target_process_list = _process_list

    def pick(self):
        exist_process_list = []
        for process in psutil.process_iter():
            exist_process_list.append(process.name())

        not_found_list = []
        for name in self.target_process_list:
            if name not in exist_process_list:
                not_found_list.append(name)

        if len(not_found_list):
            self.data_report['value'] = 1
            self.data_report['message'] = 'not found:' + ','.join(not_found_list)

def main_test():
    picker_list = []
    picker_list.append(CpuDataPicker())
    picker_list.append(MemoryDataPicker())
    picker_list.append(NetworkDataPicker(1))
    picker_list.append(NetworkDataPicker(2))
    process_list = ['fteproxy.bin', 'nginx', 'notfound']
    picker_list.append(ProcessPicker(process_list))

    for picker in picker_list:
        picker.start()

    while(True):
        os.system('clear')
        for picker in picker_list:
            cur_data = picker.fetch_data()
            print cur_data
        time.sleep(1)

if __name__ == '__main__':
    main_test()
