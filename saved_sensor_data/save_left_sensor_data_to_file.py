import socket
import requests


SENSORS = {
    'left': {
        'ip': '192.168.1.12',
        'output_filename': 'left_sensor.bin',
        'output_port': 54321
    },

    'right': {
        'ip' : '192.168.1.11',
        'output_filename': 'right_sensor.bin',
        'output_port': 54322
    },

    'top': {
        'ip': '192.168.1.13',
        'output_filename': 'top_sensor.bin',
        'output_port': 54323
    }
}

ADDRESS = '192.168.1.50'

for elem in SENSORS.values(): 
    if elem['ip'] == '192.168.1.12':
        REQUEST_HANDLE_UDP = requests.get(f'http://{elem["ip"]}/cmd/request_handle_udp?address=192.168.1.50&port={elem["output_port"]}&packet_type=A')
        r = REQUEST_HANDLE_UDP.json()
        print(f'Handle for IP {elem["ip"]} is: ' + str(r['handle']))

        REQUEST_SET_PARAMS = requests.get(f'http://{elem["ip"]}/cmd/set_scanoutput_config?handle={r["handle"]}&max_num_points_scan=1800')
        r_sp = REQUEST_SET_PARAMS.json()
        print(r_sp)

        REQUEST_START_SCANOUPUT = requests.get(f'http://{elem["ip"]}/cmd/start_scanoutput?handle={r["handle"]}')
        r_so = REQUEST_START_SCANOUPUT.json()
        print(r_so)

        sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
        sock.bind((ADDRESS, elem["output_port"]))

        i=1
        while True:
            print('Loop number: ' + str(i))
            data, addr = sock.recvfrom(65536)
            with open(elem['output_filename'], 'ab') as file:
                file.write(data)
            i = i+1
