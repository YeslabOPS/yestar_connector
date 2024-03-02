from utils import *

mysql = MySQL()
influx = Influx()


def if_proc(data: list) -> list:
    if_status = []
    for if_dict in data:
        if "up" not in if_dict["status"]:
            if_status.append(if_dict["name"])
    return if_status


def route_proc(data: str):
    route_table = []
    for route in data.split('\n'):
        flag = None
        if route.startswith(" "):
            route = route.strip()
        if route[1:].startswith(" "):
            flag = route[0]
            route = route[1:].strip()
        if "Direct" in route:
            flag = 'C'
        if "Static" in route:
            flag = 'S'
        net, info = route.split()[0], route.split()[-1]
        if "subnets" in route:
            info = route.split("subnetted, ")[1]
        route_table.append([net, flag, info])
    if route_table:
        route_df = pd.DataFrame(route_table, columns=['Network',
                                                      'Flag',
                                                      'Info'])
        mysql.write(route_df, 'RouteTable')


def cpu_proc(device_ip: str, data: dict):
    for metric in data:
        cpu_v = int(data[metric].split('%')[0])
        influx.write(device_ip, (metric, cpu_v))
