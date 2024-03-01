import uvicorn
from pydantic import BaseModel
from fastapi import FastAPI
from configbk import ConfigManager
from dataproc import if_proc, route_proc, cpu_proc
from automation import if_auto

app = FastAPI()

agent_ip = "127.0.0.1"
config_manager = ConfigManager()


class Interfaces(BaseModel):
    name: str
    ip: str
    status: str


class Monitor(BaseModel):
    cpu1_5s: str
    cpu2_5s: str
    cpu1_1m: str
    cpu1_5m: str


class AgentData(BaseModel):
    deviceIp: str
    config: str | None = None
    interfaces: list[Interfaces] = list()
    routeTable: str | None = None
    monitor: dict[str, Monitor] = dict()


@app.post("/api/data")
async def api_connect(data: AgentData):
    ip = data["device_ip"]
    if data["config"]:
        config_manager.backup(ip, data["config"])
    if data["interfaces"]:
        auto_up_list = if_proc(data["interfaces"])
        for if_name in auto_up_list:
            result = if_auto(agent_ip, data["deviceIp"], if_name)
            if result == "OK":
                print(f"Device {data["deviceIp"]} interface {if_name} fixed")
            else:
                print(result)
    if data["routeTable"]:
        route_proc(data["routeTable"])
    if data["monitor"]:
        for cpu_name in data["monitor"]:
            cpu_proc(data["deviceIp"], data["monitor"][cpu_name])


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000, log_level="info")
