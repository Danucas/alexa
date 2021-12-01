import os
import json


def save_status(device_id, st, code=None, data=None):
    stats = get_status(device_id)
    stats['code'] = code
    stats['action'] = st
    if data:
        stats['data'] = data
    status_path = f'{os.getcwd()}/sessions/{device_id}.status'
    with open(status_path, 'w') as status_file:
        status_file.write(json.dumps(stats))
    print(f'Status saved in {status_path}')


def get_status(device_id):
    try:
        status_path = f'{os.getcwd()}/sessions/{device_id}.status'
        with open(status_path, 'r') as status_file:
            return json.loads(status_file.read())
    except:
        return {'action': ''}
