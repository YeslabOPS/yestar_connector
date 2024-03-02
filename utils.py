import os
import influxdb_client
import pandas as pd
from sqlalchemy import create_engine
from influxdb_client.client.write_api import SYNCHRONOUS


class MySQL:
    def __init__(self):
        self.user = os.environ.get('MYSQL_USER')
        self.secr = os.environ.get('MYSQL_PASS')
        self.host = os.environ.get('MYSQL_HOST')
        self.db = os.environ.get('MYSQL_DB')
        #self.connect()

    def connect(self):
        self.sql_con = create_engine(f"mysql+pymysql://{self.user}:{self.secr}@{self.host}:3306/{self.db}")

    def write(self, pd_data: pd.DataFrame, tb_name: str, exists='replace'):
        pd_data.to_sql(name=tb_name, con=self.sql_con, if_exists=exists, index=False)

    def read(self, tb_name: str):
        pd.read_sql(sql=tb_name, con=self.sql_con)


class Influx:
    def __init__(self):
        self.host = f"http://{os.environ.get('INFLUX_HOST')}:8086"
        self.org = os.environ.get('INFLUX_ORG')
        self.bucket = os.environ.get('INFLUX_BUCKET')
        self.token = os.environ.get('INFLUX_TOKEN')

        client = influxdb_client.InfluxDBClient(url=self.host, token=self.token, org=self.org)
        self.write_api = client.write_api(write_options=SYNCHRONOUS)
        self.query_api = client.query_api()

    def write(self, pname, field_tup):
        data_point = influxdb_client.Point(pname).field(field_tup[0], field_tup[1])
        self.write_api.write(bucket=self.bucket, org=self.org, record=data_point)

    def query(self, flux_query: str):
        return self.query_api.query(query=flux_query)
