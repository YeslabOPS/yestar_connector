from utils import *

mysql = MySQL()
influx = Influx()


def if_proc(data: list):
    if_status = []
    for if_dict in data:
        if if_dict['status'] != 'up':
            if_status.append(if_dict['name'])
    return if_status


def route_proc(data: str):
    route_table = []
    for route in data.split('\n'):
        if route.startswith(''):
            flag = 'Subnet'
            other_part = route.strip()
            info = ' and '.join(other_part.split(', ')[-2:])
        else:
            flag = route[0]
            other_part = route[1:].strip()
            info = other_part.split(', ')[-1]
        net = other_part.split()[0]
        route_table.append([net, flag, info])
    if route_table:
        route_df = pd.DataFrame(route_table, columns=['Network', 'Flag', 'Info'])
        mysql.write(route_df, 'RouteTable')


def cpu_proc(device_ip: str, data: dict):
    for metric in data:
        cpu_v = int(data[metric])
        influx.write(device_ip, (metric, cpu_v))
