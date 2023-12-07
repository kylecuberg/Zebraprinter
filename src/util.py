# Standard library
from os import getenv
from socket import AF_INET, SOCK_STREAM, socket

# Third-party
from pandas import read_sql_query
from sqlalchemy import create_engine, text
from zebra import Zebra

# First-party/Local
from private import (
    mysql_host,
    mysql_password,
    mysql_user,
    zt411_host,
    zt411_port,
    zt421_dpi,
)


class generalized_barcode_generation:
    def __init__(self, label_x=2, label_y=1, dpi=203):
        """create zebra printer string for the barcode labels.
        Run .wo_based, .excel_based, or .manual to generate the entry.
        Run .send to create the individual zebra strings & print
        """
        self.label_x = int(label_x)
        self.label_y = int(label_y)
        self.dpi = int(dpi)
        self.zitems = {}
        self.qr = ""

    def entered(self, value=None, check_override=False, **kwargs):
        try:
            if value is None:
                item_list = [
                    "".join(
                        str(
                            input(
                                kwargs.get(
                                    "string_override",
                                    "Please type in Workorder, Barcode OR Cell_ID to print labels for: ",
                                )
                            )
                        ).strip()
                    )
                ]
            else:
                if value is list:
                    item_list = value
                else:
                    item_list = [value]
            if not check_override:
                self.zitems = self.item_check(item_list)
            else:
                self.zitems = self.no_check(item_list)
            self.celllabel()
        except Exception as E:
            print(E, type(E).__name__, __file__, E.__traceback__.tb_lineno)
        return item_list

    def _dpi(self, **kwargs):
        return int(kwargs.get("dpi", self.dpi))

    def no_check(self, item_list):
        d = {}
        for item in item_list:
            d[item] = {"workorder": "", "barcode": ""}
        return d

    def item_check(self, item_list):
        d = {}
        try:
            sparc = MySQL(
                getenv("mysql_user", mysql_user),
                getenv("mysql_password", mysql_password),
                getenv("mysql_host", mysql_host),
                database=getenv("mysql_database", "sparc"),
            )

            for item in item_list:
                cell_info_list = sparc.select(
                    rf"""select
                    CASE WHEN t.thingname like 'CHG%%' THEN NULL ELSE t.thingname END AS cell_id,
                    t.workorder,
                    CASE WHEN g.thingname like 'CHG%%' THEN ''
                    WHEN t.workorder like 'WO%%' THEN ''
                    ELSE g.thingname END AS raw
                    from sparc.thing t
                    inner join sparc.genealogy g on g.parentthingname = t.thingname
                    where t.thingname like '{item}' or g.thingname like '{item}' or t.workorder like '{item}'
                    group by cell_id, t.workorder, raw
                    order by cell_id desc, raw asc
                    """
                ).values.tolist()
                if len(cell_info_list) == 0:
                    print(f"nothing was found with the name {item}")
                for cell_info in cell_info_list:
                    if cell_info[2] != "":
                        cell_info[2] = "Raw-" + cell_info[2]
                    d[cell_info[0]] = {"workorder": cell_info[1], "barcode": cell_info[2]}
        except Exception as E:
            print(E, type(E).__name__, __file__, E.__traceback__.tb_lineno)
        return d

    def celllabel(self, **kwargs):
        try:
            for key, item in self.zitems.items():
                qr = self._cell_zebra_text(
                    cell=key,
                    barcode=item.get("barcode", ""),
                    workorder=item.get("workorder", ""),
                    label_x=self.label_x,
                    label_y=self.label_y,
                    **kwargs,
                )
                self.zitems[key]["qr"] = qr
        except Exception as E:
            print(E, type(E).__name__, __file__, E.__traceback__.tb_lineno)

    def _cell_zebra_text(self, **kwargs):
        """Zebra printer configuration
            **kwargs: qr_loc, cell_loc, barcode_loc, workorder_loc, cell_text_size, barcode_text_size, workorder_text_size
        Returns:
            _type_: _description_
        """
        try:
            if "dpi" in kwargs:
                self.dpi = self._dpi(dpi=kwargs.get("dpi", self.dpi))
            else:
                self.dpi = self._dpi()
            qr_loc = str(kwargs.get("qr_loc", str(round(0.250 * self.dpi, 0)) + "," + str(round(0.200 * self.dpi, 0))))
            cell_loc = str(
                kwargs.get("cell_loc", str(round(0.800 * self.dpi, 0)) + "," + str(round(0.246 * self.dpi, 0)))
            )
            barcode_loc = str(
                kwargs.get("barcode_loc", str(round(0.800 * self.dpi, 0)) + "," + str(round(0.575 * self.dpi, 0)))
            )
            workorder_loc = str(
                kwargs.get("workorder_loc", str(round(0.665 * self.dpi, 0)) + "," + str(round(0.739 * self.dpi, 0)))
            )
            cell_text_size = str(
                kwargs.get("cell_text_size", str(round(0.200 * self.dpi, 0)) + "," + str(round(0.180 * self.dpi, 0)))
            )
            barcode_text_size = str(
                kwargs.get("barcode_text_size", str(round(0.100 * self.dpi, 0)) + "," + str(round(0.100 * self.dpi, 0)))
            )
            workorder_text_size = str(
                kwargs.get(
                    "workorder_text_size", str(round(0.200 * self.dpi, 0)) + "," + str(round(0.180 * self.dpi, 0))
                )
            )
            self.qr = f"""^XA
                ^FO{qr_loc},0^BQN,2,4,Q,7^FDQA,{kwargs.get("cell", "")}^FS
                ^CF0,{cell_text_size}^FO{cell_loc},0^FB250,8,0,L,0^FD{kwargs.get("cell", "")}^FS
                ^CF0,{barcode_text_size}^FO{barcode_loc},0^FD{kwargs.get("barcode", "")}^FS
                ^CF0,{workorder_text_size}^FO{workorder_loc},0^FD{kwargs.get("workorder", "")}^FS
                ^XZ"""
        except Exception as E:
            print(E, type(E).__name__, __file__, E.__traceback__.tb_lineno)
        return self.qr

    def productionboxlabel(self, cell_id):
        sparc = MySQL(
            getenv("mysql_user", mysql_user),
            getenv("mysql_password", mysql_password),
            getenv("mysql_host", mysql_host),
            database=getenv("mysql_database", "sparc"),
        )
        try:
            cell_no_pn = cell_id.split(":", 1)[1]
            cell_list = sparc.select(
                rf"""select workorder, 'N/A' as batch, p.partnumber, location
                from sparc.thing t
                inner join sparc.part p on p.id = t.partid
                where t.thingname like '%%{cell_no_pn}'
                Group by workorder, p.partnumber, location
                UNION
                select i.lot as workorder, coalesce(r.batch,'N/A') as batch, i.cellformat as partnumber, i.location
                from sparc.incomingcell i
                left join sparc.receiving r on r.po = i.po and r.lp = i.lp
                where i.barcode like '%%{cell_id}'
                group by i.lot, i.cellformat, i.location, r.batch"""
            ).values.tolist()
            for row in cell_list:
                lot = row[0]
                batch = row[1]
                cellformat = row[2]
                celllocation = row[3]
                self.label_y = 2
                self.label_x = 3
                self.dpi = getenv("zt421_dpi", zt421_dpi)
                self.zitems[cell_id] = {"qr": self._productionbox_zebra_text(lot, batch, cellformat, celllocation)}
        except Exception as E:
            print(E, type(E).__name__, __file__, E.__traceback__.tb_lineno)

    def _productionbox_zebra_text(self, lot, batch, cellformat, celllocation, **kwargs):
        try:
            if "dpi" in kwargs:
                self.dpi = self._dpi(dpi=kwargs.get("dpi", self.dpi))
            else:
                self.dpi = self._dpi()
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

    def processboxlabel(self, cell_id, qty):
        sparc = MySQL(
            getenv("mysql_user", mysql_user),
            getenv("mysql_password", mysql_password),
            getenv("mysql_host", mysql_host),
            database=getenv("mysql_database", "sparc"),
        )
        try:
            cell_list = sparc.select(
                rf"""select workorder, 'N/A' as batch, p.partnumber, location
                    from sparc.thing t
                    inner join sparc.part p on p.id = t.partid
                    where CONCAT(p.partnumber,':',t.thingname) like '{cell_id}'
                    or t.thingname like '{cell_id}'
                    group by workorder, p.partnumber, location"""
            ).values.tolist()

            for row in cell_list:
                lot = row[0]
                batch = row[1]
                cellformat = row[2]
                celllocation = row[3]
                self.label_y = 2
                self.label_x = 3
                self.dpi = getenv("zt421_dpi", zt421_dpi)
                self.zitems[cell_id] = {"qr": self._processbox_zebra_text(lot, batch, cellformat, celllocation, qty)}
        except Exception as E:
            print(E, type(E).__name__, __file__, E.__traceback__.tb_lineno)

    def _processbox_zebra_text(self, lot, batch, cellformat, celllocation, qty, **kwargs):
        try:
            if "dpi" in kwargs:
                self.dpi = self._dpi(dpi=kwargs.get("dpi", self.dpi))
            else:
                self.dpi = self._dpi()
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

    def send(self, **kwargs):
        try:
            z = zebra(**kwargs)
            if "qr" in kwargs:
                z.qr = kwargs.get("qr")
                z.send(**kwargs)
            else:
                for key, item in self.zitems.items():
                    z.qr = item["qr"]
                    z.send(**kwargs)
        except Exception as E:
            print(E, type(E).__name__, __file__, E.__traceback__.tb_lineno)

    def reset(self):
        self.zitems = {}
        self.item_list = []


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
            df = read_sql_query(text(query_text), con=self.engine)
        except Exception as E:
            print(E, type(E).__name__, __file__, E.__traceback__.tb_lineno)
            df = None
        return df


class zebra:
    def __init__(self, **kwargs):
        self.qr = kwargs.get("qr", "")
        self.name = kwargs.get("printer_name", "")
        self.conn_type = kwargs.get("conn_type", "ip")

    def _check_host_port(self, host, port):
        if host == "":
            host = getenv("ops_host", zt411_host)
        if port == "":
            port = int(getenv("ops_port", zt411_port))
        return host, port

    def create_ip_conn(self, **kwargs):
        try:
            sock = socket(AF_INET, SOCK_STREAM)
            host, port = self._check_host_port(kwargs.get("host", ""), kwargs.get("port", ""))
            sock.connect((host, int(port)))
        except Exception as E:
            print(type(E).__name__, __file__, E.__traceback__.tb_lineno, "\n", E)
        return sock

    def create_blue_conn(self, **kwargs):
        try:
            sock = socket(AF_INET, SOCK_STREAM)
            host, port = self._check_host_port(kwargs.get("host", ""), kwargs.get("port", ""))
            sock.connect((host, int(port)))
        except Exception as E:
            print(type(E).__name__, __file__, E.__traceback__.tb_lineno, "\n", E)
        return sock

    def send(self, **kwargs):
        try:
            if self.conn_type == "name":
                z = Zebra()
                z.setqueue(self.name)
                z.output(self.qr)
                return None
            elif self.conn_type == "ip":
                self.sock = self.create_ip_conn(host=kwargs.get("host", ""), port=kwargs.get("port", ""))
            elif self.conn_type == "bluetooth":
                self.sock = self.create_blue_conn(host=kwargs.get("host", ""), port=kwargs.get("port", ""))
            self.sock.send(bytes(self.qr, "utf-8"))  # using bytes
            self.sock.close()
        except Exception as E:
            print(E, type(E).__name__, __file__, E.__traceback__.tb_lineno)


def main():
    try:
        print("generalized_cell.py")
    except Exception as E:
        print(E, type(E).__name__, __file__, E.__traceback__.tb_lineno)
        input("Press Enter to close")


if __name__ == "__main__":
    main()
