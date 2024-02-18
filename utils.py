import os
import influxdb_client
from sqlalchemy import create_engine
from influxdb_client.client.write_api import SYNCHRONOUS


# MySQL Info


class Influx:
    def __init__(self, server, org, bucket):
        self.org = org
        self.bucket = bucket
        token = os.environ.get('INFLUX_TOKEN')
        influx_server = self.server
        client = influxdb_client.InfluxDBClient(url=influx_server, token=token, org=self.org)
        self.api_writer = client.write_api(write_options=SYNCHRONOUS)

    def write(self, pname, field_tup):
        data_point = influxdb_client.Point(pname).field(field_tup[0], field_tup[1])
        self.api_writer.write(bucket=self.bucket, org=self.org, record=data_point)

class MySQL:
    def __init__(self, server):
        mysql_user = os.environ.get('MYSQL_USER')
        mysql_pass = os.environ.get('MYSQL_PASS')
        mysql_host = "192.168.1.50"
        mysql_db = "Meraki"

    def write(self, pd_data, tb_name, exists='replace'):
        sql_con = create_engine(f"mysql+pymysql://{mysql_user}:{mysql_pass}@{mysql_host}:3306/{mysql_db}")
        pd_data.to_sql(name=tb_name, con=sql_con, if_exists=exists, index=False)