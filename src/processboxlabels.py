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

                label = util.qr_text(label_x=3, label_y=2, dpi=os.getenv("zt421_dpi", private.zt421_dpi))
                qr = label.process_boxlabel(lot, batch, cellformat, celllocation, qty)
                z = util.zebra(qr)
                z.send(
                    host=os.getenv("zt421_host", private.zt421_host), port=os.getenv("zt421_port", private.zt421_port)
                )

    except Exception as E:
        print(E, type(E).__name__, __file__, E.__traceback__.tb_lineno)
