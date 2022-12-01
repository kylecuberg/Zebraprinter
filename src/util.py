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

    def create_ip_conn(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((os.getenv("ops_host", private.ops_host), int(os.getenv("ops_port", private.ops_port))))
        except Exception as E:
            print(type(E).__name__, __file__, E.__traceback__.tb_lineno, "\n", E)
        return sock

    def create_blue_conn(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((os.getenv("ops_host"), int(os.getenv("ops_port"))))
        except Exception as E:
            print(type(E).__name__, __file__, E.__traceback__.tb_lineno, "\n", E)
        return sock

    def send(self):
        if self.conn_type == "ip":
            self.sock = self.create_ip_conn()
        elif self.conn_type == "bluetooth":
            self.sock = self.create_blue_conn()
        self.sock.send(bytes(self.qr, "utf-8"))  # using bytes
        self.sock.close()


def loop_csv_file(filename):
    lines = []
    with open(filename) as read_obj:
        for row in csv.reader(read_obj):
            lines.append(row)
    return lines


def loop_xlsb_file(filename="input/Print_File.xlsb", sheetname="PRINT"):
    li = []
    with open_workbook(filename) as wb:
        with wb.get_sheet(sheetname) as sheet:
            for row in sheet.rows():
                val = [r.v for r in row]
                li.append(val[0])  # retrieving content
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
