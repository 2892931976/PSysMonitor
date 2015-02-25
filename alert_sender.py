import tonggao_sdk_py

def send_alert(message):
    service_id = '952'
    service_key = 'f566462643b4d90d5e6f9134d0ba441d'
    tonggaoIncident = tonggao_sdk_py.TonggaoIncident(service_id, service_key)
    tonggaoIncident.triggerIncident(message)

