# Standard library
import os

# First-party/Local
import private
import util

if __name__ == "__main__":
    """[summary]"""

    try:
        # get from sql
        sparc = util.MySQL(
            os.getenv("mysql_user", private.mysql_user),
            os.getenv("mysql_password", private.mysql_password),
            os.getenv("mysql_host", private.mysql_host),
            database=os.getenv("mysql_database", "sparc"),
        )

        while True:
            cell = str(input("Please type in cell_id to print box label for: "))
            qty = str(input("Please type in the QUANTITY of cells in the box:  "))

            cell_list = sparc.select(
                rf"""select i.lot, coalesce(r.batch,'N/A'), i.cellformat, i.location
                                     from sparc.incomingcell i
                                     left join sparc.receiving r on r.po = i.po and r.lp = i.lp
                                     where i.barcode like '{cell}'
                                     group by i.lot, i.cellformat, i.location, r.batch"""
            ).values.tolist()

            for row in cell_list:
                lot = row[0]
                batch = row[1]
                cellformat = row[2]
                celllocation = row[3]

                label = util.qr_text(dpi=203)
                z = util.zebra(qr=label.process_boxlabel(lot, batch, cellformat, celllocation, qty))
                z.send(host=os.get_env("zt421_host", ""), port=os.get_env("zt421_port", ""))
                # qr =
                f"""^XA
                    ^CF0,40,32^FO20,20,0^FDLot:^FS
                    ^CF0,40,32^FO20,100,0^FDBatch:^FS
                    ^CF0,40,32^FO20,180,0^FDFormat:^FS
                    ^CF0,40,32^FO20,260,0^FDLocation:^FS
                    ^CF0,40,32^FO20,340,0^FDQty:^FS
                    ^GB700,0,1,B,1^FO0,80,0^FS
                    ^GB700,0,1,B,1^FO0,160,0^FS
                    ^GB700,0,1,B,1^FO0,240,0^FS
                    ^GB700,0,1,B,1^FO0,320,0^FS
                    ^CF0,40,32^FO550,20,1^FD{lot}^FS
                    ^CF0,40,32^FO550,100,1^FD{batch}^FS
                    ^CF0,40,32^FO550,180,1^FD{cellformat}^FS
                    ^CF0,40,32^FO550,260,1^FD{celllocation}^FS
                    ^CF0,40,32^FO550,340,1^FD{qty}^FS
                    ^XZ"""
                # z = util.zebra(qr=qr)
                # z.send(host=os.get_env("zt421_host", ""), port=os.get_env("zt421_port", ""))

    except Exception as E:
        print(E, type(E).__name__, __file__, E.__traceback__.tb_lineno)
