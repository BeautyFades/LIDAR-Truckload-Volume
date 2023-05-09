import requests


def request_handle_udp(
                    sensor_address:str,
                    client_port:int,
                    client_address:str = '192.168.1.50',
                    watchdog:str = 'off', # Whether or not to use watchdog (on/off)
                    watchdog_timeout:int = 60000, # Timeout in ms if using watchdog
                    packet_type:str = 'A',
                    start_angle:int = -1800000,
                    max_num_points_scan:int = 0,
                    skip_scans:int = 0,
                    ) -> dict:

    params = {
        'address': client_address,
        'port': client_port,
        'packet_type': packet_type,
        
        'watchdog': watchdog,
        'watchdogtimeout': watchdog_timeout,
        'start_angle': start_angle,
        'max_num_points_scan': max_num_points_scan,
        'skip_scans': skip_scans,
    }

    REQUEST_HANDLE_UDP = requests.get(f'http://{sensor_address}/cmd/request_handle_udp', params=params)
    r = REQUEST_HANDLE_UDP.json()
    return r


def set_scanoutput_config(
                        sensor_address:str,
                        handle:str,
                        watchdog:str = 'off', # Whether or not to use watchdog (on/off)
                        watchdog_timeout:int = 60000, # Timeout in ms if using watchdog
                        packet_type:str = 'A',
                        start_angle:int = -1800000,
                        max_num_points_scan:int = 0,
                        skip_scans:int = 0,
                    ) -> dict:
    
    params = {
        'handle': handle,
        'watchdog': watchdog,
        'watchdogtimeout': watchdog_timeout,
        'packet_type': packet_type,
        'start_angle': start_angle,
        'max_num_points_scan': max_num_points_scan,
        'skip_scans': skip_scans,
    }

    REQUEST_SET_PARAMS = requests.get(f"http://{sensor_address}/cmd/set_scanoutput_config", params=params)
    r = REQUEST_SET_PARAMS.json()
    return r


def start_scanoutput(
                    sensor_address:str,
                    handle:str,
                ) -> dict:
    
    params = {
        'handle': handle,
    }

    REQUEST_START_SCANOUTPUT = requests.get(f"http://{sensor_address}/cmd/start_scanoutput", params=params)
    r = REQUEST_START_SCANOUTPUT.json()
    return r


def stop_scanoutput(
                    sensor_address:str,
                    handle:str,
                ) -> dict:
    
    params = {
        'handle': handle,
    }

    REQUEST_STOP_SCANOUTPUT = requests.get(f"http://{sensor_address}/cmd/stop_scanoutput", params=params)
    r = REQUEST_STOP_SCANOUTPUT.json()
    return r


def get_parameters(
                    sensor_address:str,
                ) -> dict:

    REQUEST_GET_PARAMS = requests.get(f"http://{sensor_address}/cmd/get_parameter")
    r = REQUEST_GET_PARAMS.json()
    return r








