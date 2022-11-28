# Standard library
import csv
import os
import socket

# Third-party
from pyxlsb import open_workbook


class zebra:
    def __init__(self, qr, conn_type="ip"):
        self.qr = qr
        self.conn_type = conn_type

    def create_ip_conn(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(("172.16.99.203", 6101))
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


def loop_xlsb_file(filename="input/Print_File.xlsb"):
    li = []
    with open_workbook(filename) as wb:
        with wb.get_sheet("PRINT") as sheet:
            for row in sheet.rows():
                val = [r.v for r in row]
                li.append(val[0])  # retrieving content
    return li[1:]
