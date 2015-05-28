import tonggao_sdk_py

def send_alert(message):
    service_id = '952'
    service_key = '4164fe4dba67ed7d5bf057e43ac67db5'
    tonggaoIncident = tonggao_sdk_py.TonggaoIncident(service_id, service_key)
#No more incident
    #tonggaoIncident.triggerIncident(message)

