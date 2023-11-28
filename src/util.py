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
    def __init__(self, qr, **kwargs):
        self.qr = qr
        self.conn_type = kwargs.get("conn_type", "ip")

    def _check_host_port(self, host, port):
        if host == "":
            host = os.getenv("ops_host", private.zt411_host)
        if port == "":
            port = int(os.getenv("ops_port", private.zt411_port))
        return host, port

    def create_ip_conn(self, **kwargs):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            host, port = self._check_host_port(kwargs.get("host", ""), kwargs.get("port", ""))
            sock.connect((host, int(port)))
        except Exception as E:
            print(type(E).__name__, __file__, E.__traceback__.tb_lineno, "\n", E)
        return sock

    def create_blue_conn(self, **kwargs):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            host, port = self._check_host_port(kwargs.get("host", ""), kwargs.get("port", ""))
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


class qr_text:
    def __init__(self, dpi=203, label_x=2, label_y=1, **kwargs):
        try:
            self.dpi = int(dpi)
            self.label_x = float(label_x)
            self.label_y = float(label_y)
            self.qr = ""
        except Exception as E:
            print(E, type(E).__name__, __file__, E.__traceback__.tb_lineno)

    def sn_barcode(self, cell, barcode):
        qr_loc = str(round(0.075 * self.dpi, 0)) + "," + str(round(0.2 * self.dpi, 0))
        cell_loc = str(round(0.665 * self.dpi, 0)) + "," + str(round(0.45 * self.dpi, 0))
        barcode_loc = str(round(0.665 * self.dpi, 0)) + "," + str(round(0.8 * self.dpi, 0))
        cell_text_size = str(round(0.2 * self.dpi, 0)) + "," + str(round(0.16 * self.dpi, 0))
        barcode_text_size = str(round(0.1 * self.dpi, 0)) + "," + str(round(0.1 * self.dpi, 0))
        self.qr = f"""^XA
            ^FO{qr_loc},0^BQN,2,5,Q,7^FDQA,{cell}^FS
            ^CF0,{cell_text_size}^FO{cell_loc},0^FD{cell}^FS
            ^CF0,{barcode_text_size}^FO{barcode_loc},0^FDRaw-{barcode}^FS
            ^XZ"""
        return self.qr

    def sn_workorder(self, cell, workorder):
        qr_loc = str(round(0.075 * self.dpi, 0)) + "," + str(round(0.2 * self.dpi, 0))
        cell_loc = str(round(0.665 * self.dpi, 0)) + "," + str(round(0.45 * self.dpi, 0))
        workorder_loc = str(round(0.665 * self.dpi, 0)) + "," + str(round(0.8 * self.dpi, 0))
        cell_text_size = str(round(0.2 * self.dpi, 0)) + "," + str(round(0.16 * self.dpi, 0))
        workorder_text_size = str(round(0.2 * self.dpi, 0)) + "," + str(round(0.16 * self.dpi, 0))
        self.qr = f"""^XA
            ^FO{qr_loc},0^BQN,2,5,Q,7^FDQA,{cell}^FS
            ^CF0,{cell_text_size}^FO{cell_loc},0^FD{cell}^FS
            ^CF0,{workorder_text_size}^FO{workorder_loc},0^FD{workorder}^FS
            ^XZ"""
        return self.qr

    def sn_combo(self, cell, barcode, workorder, **kwargs):
        """create sn zebra printer format text with cell_id, barcode, workorder

        Args:
            cell (str): name of cell
            barcode (str): name of barcode / child
            workorder (str): name of workorder

        Returns:
            str : string that represents the zebra printer code for the label
        """
        qr_loc = str(kwargs.get("qr_loc", str(round(0.075 * self.dpi, 0)) + "," + str(round(0.2 * self.dpi, 0))))
        cell_loc = str(kwargs.get("cell_loc", str(round(0.665 * self.dpi, 0)) + "," + str(round(0.246 * self.dpi, 0))))
        barcode_loc = str(
            kwargs.get("barcode_loc", str(round(0.665 * self.dpi, 0)) + "," + str(round(0.542 * self.dpi, 0)))
        )
        workorder_loc = str(kwargs.get("", str(round(0.665 * self.dpi, 0)) + "," + str(round(0.739 * self.dpi, 0))))
        cell_text_size = str(
            kwargs.get("cell_text_size", str(round(0.2 * self.dpi, 0)) + "," + str(round(0.16 * self.dpi, 0)))
        )
        workorder_text_size = str(
            kwargs.get("workorder_text_size", str(round(0.2 * self.dpi, 0)) + "," + str(round(0.2 * self.dpi, 0)))
        )
        barcode_text_size = str(
            kwargs.get("barcode_text_size", str(round(0.2 * self.dpi, 0)) + "," + str(round(0.16 * self.dpi, 0)))
        )
        self.qr = f"""^XA
            ^FO{qr_loc},0^BQN,2,5,Q,7^FDQA,{cell}^FS
            ^CF0,{cell_text_size}^FO{cell_loc},0^FD{cell}^FS
            ^CF0,{barcode_text_size}^FO{barcode_loc},0^FD{barcode}^FS
            ^CF0,{workorder_text_size}^FO{workorder_loc},0^FD{workorder}^FS
            ^XZ"""
        return self.qr

    def boxlabel(self, lot, batch, cellformat, celllocation, **kwargs):
        try:
            text_size = str(
                kwargs.get("text_size", f"{str(round(self.dpi * 0.3, 0))},{str(round(self.dpi * 0.256, 0))}")
            )
            self.qr = f"""^XA
                    ^CF0,{text_size}^FO20,{str(0.1 * self.dpi)},0^FDLot:^FS
                    ^CF0,{text_size}^FO20,{str(0.6 * self.dpi)},0^FDBatch:^FS
                    ^CF0,{text_size}^FO20,{str(1.1 * self.dpi)},0^FDFormat:^FS
                    ^CF0,{text_size}^FO20,{str(1.6 * self.dpi)},0^FDLocation:^FS
                    ^GB{str(self.label_x * self.dpi)},0,1,B,1^FO0,{str(0.5 * self.dpi)},0^FS
                    ^GB{str(self.label_x * self.dpi)},0,1,B,1^FO0,{str(1 * self.dpi)},0^FS
                    ^GB{str(self.label_x * self.dpi)},0,1,B,1^FO0,{str(1.5 * self.dpi)},0^FS
                    ^CF0,{text_size}^FO{str(0.9*self.label_x * self.dpi)},{str(0.1 * self.dpi)},1^FD{lot}^FS
                    ^CF0,{text_size}^FO{str(0.9*self.label_x * self.dpi)},{str(0.6 * self.dpi)},1^FD{batch}^FS
                    ^CF0,{text_size}^FO{str(0.9*self.label_x * self.dpi)},{str(1.1 * self.dpi)},1^FD{cellformat}^FS
                    ^CF0,{text_size}^FO{str(0.9*self.label_x * self.dpi)},{str(1.6 * self.dpi)},1^FD{celllocation}^FS
                    ^XZ"""
        except Exception as E:
            print(E, type(E).__name__, __file__, E.__traceback__.tb_lineno)
        return self.qr

    def process_boxlabel(self, lot, batch, cellformat, celllocation, qty, **kwargs):
        try:
            text_size = str(kwargs.get("text_size", f"{str(round(self.dpi * 0.3, 0))},{str(round(self.dpi * 0.3, 0))}"))
            self.qr = f"""^XA
                    ^CF0,{text_size}^FO20,{str(0.1 * self.dpi)},0^FDLot:^FS
                    ^CF0,{text_size}^FO20,{str(0.5 * self.dpi)},0^FDNote:^FS
                    ^CF0,{text_size}^FO20,{str(0.9 * self.dpi)},0^FDFormat:^FS
                    ^CF0,{text_size}^FO20,{str(1.3 * self.dpi)},0^FDLocation:^FS
                    ^CF0,{text_size}^FO20,{str(1.7 * self.dpi)},0^FDQty:^FS
                    ^GB{str(1.8 * self.label_x * self.dpi)},0,1,B,1^FO0,{str(0.4 * self.dpi)},0^FS
                    ^GB{str(1.8 * self.label_x * self.dpi)},0,1,B,1^FO0,{str(0.8 * self.dpi)},0^FS
                    ^GB{str(1.8 * self.label_x * self.dpi)},0,1,B,1^FO0,{str(1.2 * self.dpi)},0^FS
                    ^GB{str(1.8 * self.label_x * self.dpi)},0,1,B,1^FO0,{str(1.6 * self.dpi)},0^FS
                    ^CF0,{text_size}^FO{str(0.9*self.label_x * self.dpi)},{str(0.1 * self.dpi)},1^FD{str(lot)}^FS
                    ^CF0,{text_size}^FO{str(0.9*self.label_x * self.dpi)},{str(0.5 * self.dpi)},1^FD{str(batch)}^FS
                    ^CF0,{text_size}^FO{str(0.9*self.label_x * self.dpi)},{str(0.9 * self.dpi)},1^FD{str(cellformat)}^FS
                    ^CF0,{text_size}^FO{str(0.9*self.label_x * self.dpi)},{str(1.3 * self.dpi)},1^FD{str(celllocation)}^FS
                    ^CF0,{text_size}^FO{str(0.9*self.label_x * self.dpi)},{str(1.7 * self.dpi)},1^FD{qty}^FS
                    ^XZ"""
        except Exception as E:
            print(E, type(E).__name__, __file__, E.__traceback__.tb_lineno)
        return self.qr
