import psutil
import time

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

