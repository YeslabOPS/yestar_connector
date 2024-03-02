# Connector 项目指引
Connector项目主要完成针对Agent项目的数据接收、自动化消息传递，并完成数据的处理与存档。
* 这个项目还会完成其他云端API的数据采集
* 这个项目还会完成Grafana的可视化
* 这个项目还会对Agent项目进行完善

## 软件设计
### 需求调研
独立运行的微服务，开放API给Agent以及其他微服务使用，对接Agent的Data目录的JSON数据
* 配置数据在数据中心本地做配置备份
* 接口数据进行接口监控
  * Agent已经做了自动化UP，但需要Connector做检测并API告诉Agent做UP
* 路由表数据做路由表展示
* 监控数据做展示
  * CPU数据做统一视图的展示

### 功能梳理
数据库连接 - utils.py
* MySQL的读写
* InfluxDB的读写
自动化备份 - configbk.py
* 配置对比
* 自动存文本
* 自动解决路径存在问题
数据处理 - dataproc.py
* 接口数据处理
* 路由表数据处理
* 监控数据的处理
自动化编排 - automation.py
* 发送自动化UP消息
API主程序 - main.py
* 数据接收与拆解
* 获取下层处理结果
* 程序整体逻辑

### 软件架构
高层：API主程序
中层：数据处理，自动化备份
底层：数据库连接，自动化编排
图

### API通信设计
Connector API:
/data: POST提交数据
Agent API:
/action: POST提交自动化消息
/action_history: GET查看自动化命令的执行历史