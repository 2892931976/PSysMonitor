import tonggao_sdk_py

def send_alert(message):
    service_id = '1034'
    service_key = '1338001e0314a53059b2cb2ccc216735'
    tonggaoIncident = tonggao_sdk_py.TonggaoIncident(service_id, service_key)
    tonggaoIncident.triggerIncident(message)

