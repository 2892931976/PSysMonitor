import datetime
def log(level, message):
    log_filename = '/home/work/PSysMonitor/trace.log'
    current_time = datetime.datetime.now().strftime("%d. %B %Y %I:%M%p")
    log_info = "[%s][%s][%s]" % (current_time, level, message)
    log_file = open(log_filename, 'a')
    log_file.write(log_info+'\n')
    log_file.close()
    print log_info
