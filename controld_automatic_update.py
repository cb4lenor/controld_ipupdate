import os
import requests
import time

# Load environment variables
CONTROL_D_API_KEY = os.getenv('CONTROL_D_API_KEY')
CONTROL_D_BASE_URL = 'https://api.controld.com'
DEVICE_NAME = os.getenv('DEVICE_NAME')

def get_current_ip():
    response = requests.get('https://ifconfig.co/ip')
    response.raise_for_status()
    return response.text.strip()

def get_access_list(deviceId):
    headers = {
        "accept": "application/json",
        'Authorization': f'Bearer {CONTROL_D_API_KEY}'
        }
    params = {'device_id': deviceId}
    response = requests.get(f'{CONTROL_D_BASE_URL}/access', headers=headers, params=params)
    response.raise_for_status()
    return response.json()["body"]["ips"]

def get_devices():
    headers = {
        "accept": "application/json",
        'Authorization': f'Bearer {CONTROL_D_API_KEY}'
        }
    response = requests.get(f'{CONTROL_D_BASE_URL}/devices', headers=headers)
    response.raise_for_status()
    return response.json()["body"]["devices"]

def delete_ips(deviceId, ips):
    headers = {'Authorization': f'Bearer {CONTROL_D_API_KEY}'}
    payload = {'device_id': deviceId, 'ips': ips} 
    response = requests.delete(f'{CONTROL_D_BASE_URL}/access', headers=headers, payload=payload)
    response.raise_for_status()
    return response.json()

def create_entry(ip, device_id):
    headers = {'Authorization': f'Bearer {CONTROL_D_API_KEY}'}
    data = {'ips': [ip], 'device_id': device_id}
    response = requests.post(f'{CONTROL_D_BASE_URL}/access', headers=headers, json=data)
    print(response.text)    
    response.raise_for_status()
    return response.json()

def find_device_by_name(devices, name):
    return next((device for device in devices if device['name'] == name), None)

def main():
    old_ip = None
    while True:
        print("cb4lenor says hi!")
        try:
            current_ip = get_current_ip()
            if old_ip == current_ip:
                print("No IP change detected.")
            else:
                print("current_ip: ", current_ip)
                devices = get_devices()
                deviceId = find_device_by_name(devices, DEVICE_NAME)["device_id"]
                print("deviceID: ", deviceId)
                access_list = get_access_list(deviceId)
                print("access_list: ", access_list)
                if not access_list:
                    print("No access list found.")
                    create_entry(current_ip, deviceId)
                    print(f'Updated access list with new IP: {current_ip} for device {DEVICE_NAME}')
                elif current_ip not in [entry['ip'] for entry in access_list]:
                    print("IP change detected")
                    delete_ips(deviceId, [old_ip])
                    create_entry(current_ip, deviceId)
                    print(f'Updated access list with new IP: {current_ip} for device {DEVICE_NAME}')
                else:
                    print(f'Current IP {current_ip} is already in the access list.')
                old_ip = current_ip
        except Exception as e:
            print(f"An error occurred: {e}. Retrying in 10 minutes.")
        time.sleep(600)

if __name__ == '__main__':
    main()