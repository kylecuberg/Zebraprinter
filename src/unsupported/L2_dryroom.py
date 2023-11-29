# Standard library
from socket import AF_INET, SOCK_STREAM, socket


class zebra:
    def __init__(self, qr, **kwargs):
        self.qr = qr
        self.conn_type = kwargs.get("conn_type", "ip")
        self.host = kwargs.get("host", "192.168.10.200")
        self.port = kwargs.get("port", 6101)

    def create_ip_conn(self, **kwargs):
        try:
            sock = socket(AF_INET, SOCK_STREAM)
            sock.connect((self.host, self.port))
        except Exception as E:
            print(type(E).__name__, __file__, E.__traceback__.tb_lineno, "\n", E)
        return sock

    def send(self, **kwargs):
        try:
            self.sock = self.create_ip_conn(host=self.host, port=self.port)
            self.sock.send(bytes(self.qr, "utf-8"))  # using bytes
            self.sock.close()
        except Exception as E:
            print(E, type(E).__name__, __file__, E.__traceback__.tb_lineno)


class L2_barcode_generation:
    def __init__(self, label_x=2, label_y=1, dpi=203, **kwargs):
        """create zebra printer string for the barcode labels.
        Run .wo_based, .excel_based, or .manual to generate the entry.
        Run .send to create the individual zebra strings & print
        """
        self.label_x = int(label_x)
        self.label_y = int(label_y)
        self.dpi = int(dpi)
        self.zitems = {}
        self.host = kwargs.get("host", "192.168.10.200")
        self.port = kwargs.get("port", 6101)

    def manual(self, **kwargs):
        try:
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
            self.zitems = self.L2_items(item_list)
        except Exception as E:
            print(E, type(E).__name__, __file__, E.__traceback__.tb_lineno)
        return item_list

    def L2_items(self, item_list):
        d = {}
        try:
            for item in item_list:
                d[item] = {"workorder": "", "barcode": ""}
        except Exception as E:
            print(E, type(E).__name__, __file__, E.__traceback__.tb_lineno)
        return d

    def zebra_text(self, **kwargs):
        """Zebra printer configuration
            **kwargs: qr_loc, cell_loc, barcode_loc, workorder_loc, cell_text_size, barcode_text_size, workorder_text_size
        Returns:
            _type_: _description_
        """
        dpi = kwargs.get("dpi", self.dpi)
        qr_loc = str(kwargs.get("qr_loc", str(round(0.250 * dpi, 0)) + "," + str(round(0.200 * dpi, 0))))
        cell_loc = str(kwargs.get("cell_loc", str(round(0.800 * dpi, 0)) + "," + str(round(0.246 * dpi, 0))))
        barcode_loc = str(kwargs.get("barcode_loc", str(round(0.800 * dpi, 0)) + "," + str(round(0.575 * dpi, 0))))
        workorder_loc = str(kwargs.get("workorder_loc", str(round(0.665 * dpi, 0)) + "," + str(round(0.739 * dpi, 0))))
        cell_text_size = str(
            kwargs.get("cell_text_size", str(round(0.200 * dpi, 0)) + "," + str(round(0.180 * dpi, 0)))
        )
        barcode_text_size = str(
            kwargs.get("barcode_text_size", str(round(0.100 * dpi, 0)) + "," + str(round(0.100 * dpi, 0)))
        )
        workorder_text_size = str(
            kwargs.get("workorder_text_size", str(round(0.200 * dpi, 0)) + "," + str(round(0.180 * dpi, 0)))
        )
        self.qr = f"""^XA
            ^FO{qr_loc},0^BQN,2,4,Q,7^FDQA,{kwargs.get("cell", "")}^FS
            ^CF0,{cell_text_size}^FO{cell_loc},0^FB250,8,0,L,0^FD{kwargs.get("cell", "")}^FS
            ^CF0,{barcode_text_size}^FO{barcode_loc},0^FD{kwargs.get("barcode", "")}^FS
            ^CF0,{workorder_text_size}^FO{workorder_loc},0^FD{kwargs.get("workorder", "")}^FS
            ^XZ"""
        return self.qr

    def send(self, **kwargs):
        for key, item in self.zitems.items():
            z = zebra(
                qr=self.zebra_text(
                    cell=key,
                    barcode=item.get("barcode", ""),
                    workorder=item.get("workorder", ""),
                    label_x=self.label_x,
                    label_y=self.label_y,
                    **kwargs,
                ),
                **kwargs,
            )
            z.send(
                host=self.host,
                port=self.port,
            )

    def reset(self):
        self.zitems = {}
        self.item_list = []


if __name__ == "__main__":
    """[summary]"""
    try:
        gbg = L2_barcode_generation()
        while True:
            gbg.manual(check_override=True, string_override="Type in what to print: ")
            print(gbg.host, gbg.port)
            gbg.send()
            gbg.reset()
    except Exception as E:
        print(E, type(E).__name__, __file__, E.__traceback__.tb_lineno)

    input("Press ENTER to exit")
