from pydantic import BaseModel
from fastapi import FastAPI
from configbk import ConfigManager
from dataproc import if_proc, route_proc, cpu_proc
from automation import if_auto

import uvicorn


app = FastAPI()

agent_ip = "127.0.0.1"
config_manager = ConfigManager()


class Interfaces(BaseModel):
    name: str
    ip: str
    status: str


class CiscoCPU(BaseModel):
    cpu1_5s: str
    cpu2_5s: str
    cpu1_1m: str
    cpu1_5m: str


class HuaweiCPU(BaseModel):
    cpu_current: str
    cpu_5sec: str
    cpu_1min: str
    cpu_5min: str


class AgentData(BaseModel):
    deviceIp: str
    config: str | None = None
    interfaces: list[Interfaces] = list()
    routeTable: str | None = None
    monitor: dict[str, CiscoCPU] | dict[str, dict[str, HuaweiCPU]] = dict()


@app.post("api/data")
async def api_connect(data: AgentData):
    ip = data["deviceIp"]
    if data["config"]:
        config_manager.backup(ip, data["config"])
    if data["interfaces"]:
        auto_up_list = if_proc(data["interfaces"])
        for if_name in auto_up_list:
            result = if_auto(agent_ip, ip, if_name)
            if result == "OK":
                print(f"Device {data["deviceIp"]} interface {if_name} fixed")
            else:
                print(result)
    if data["routeTable"]:
        route_proc(data["routeTable"])
    if data["monitor"]:
        for cpu_name in data["monitor"]:
            lv1_data = data["monitor"][cpu_name]
            final_data = lv1_data
            for lv2_key in lv1_data:
                lv2_data = lv1_data[lv2_key]
                if type(lv2_data) != str:
                    final_data = lv2_data
                    cpu_proc(ip, final_data)
                else:
                    cpu_proc(ip, final_data)
                    break

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000, log_level="info")
