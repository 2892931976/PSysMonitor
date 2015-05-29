
def mail_config():
    return {
            'smtp_server':'smtp.sina.com',
            'smtp_port': 465,
            'smtp_user': 'psysmonitor',
            'smtp_password':'111222333',
            'smtp_sender': "psysmonitor<psysmonitor@sina.com>"
            }

def log_file():
    return './trace.log'

def monitor_config():
    return {
            'admin_email':'mybuffer@163.com',
            'process_list': (
                'ss-server',
                'tor',
                'nginx',
                'php5-fpm',
                'fteproxy.bin'
                ),
            'server_name':'My Server'
            }
