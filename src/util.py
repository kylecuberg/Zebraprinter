# Standard library
import csv
import os
import socket

# Third-party
import pandas as pd
from pyxlsb import open_workbook
from sqlalchemy import create_engine

# First-party/Local
import private


class zebra:
    def __init__(self, qr, conn_type="ip"):
        self.qr = qr
        self.conn_type = conn_type

    def _check_host_port(self, host, port):
        if host == "":
            host = os.getenv("ops_host", private.zt411_host)
        if port == "":
            port = int(os.getenv("ops_port", private.zt411_port))
        return host, port

    def create_ip_conn(self, **kwargs):
        host = kwargs.get("host", "")
        port = kwargs.get("port", "")
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            host, port = self._check_host_port(host, port)
            sock.connect((host, int(port)))
        except Exception as E:
            print(type(E).__name__, __file__, E.__traceback__.tb_lineno, "\n", E)
        return sock

    def create_blue_conn(self, **kwargs):
        host = kwargs.get("host", "")
        port = kwargs.get("port", "")
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            host, port = self._check_host_port(host, port)
            sock.connect((host, int(port)))
        except Exception as E:
            print(type(E).__name__, __file__, E.__traceback__.tb_lineno, "\n", E)
        return sock

    def send(self, **kwargs):
        if self.conn_type == "ip":
            self.sock = self.create_ip_conn(host=kwargs.get("host", ""), port=kwargs.get("port", ""))
        elif self.conn_type == "bluetooth":
            self.sock = self.create_blue_conn(host=kwargs.get("host", ""), port=kwargs.get("port", ""))
        self.sock.send(bytes(self.qr, "utf-8"))  # using bytes
        self.sock.close()


def loop_csv_file(filename):
    lines = []
    with open(filename) as read_obj:
        for row in csv.reader(read_obj):
            lines.append(row)
    return lines


def loop_xlsb_file(filename="input/Print_File.xlsb", sheetname="PRINT", columns=1):
    li = []
    with open_workbook(filename) as wb:
        with wb.get_sheet(sheetname) as sheet:
            try:
                for row in sheet.rows():
                    val = [r.v for r in row]
                    if val[0] is not None:
                        li.append(val[0:columns])  # retrieving content
            except Exception as E:
                print(E, type(E).__name__, __file__, E.__traceback__.tb_lineno)
    return li[1:]


class MySQL:
    def __init__(
        self,
        user,
        password,
        host,
        **kwargs,
    ):
        self.database = kwargs.get("database", "sparc")

        try:
            self.engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}/{self.database}")
        except Exception as E:
            print(E, type(E).__name__, __file__, E.__traceback__.tb_lineno)

    def select(self, query_text):
        """Get info from MySQL with select statement

        Args:
            query_text (string): Query to run

        Returns:
            Dataframe: Query results
        """
        try:
            df = pd.read_sql_query(query_text, con=self.engine)
        except Exception as E:
            print(E, type(E).__name__, __file__, E.__traceback__.tb_lineno)
            df = None
        return df
