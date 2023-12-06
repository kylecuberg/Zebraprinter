# Standard library
import os

# Third-party
import util

# First-party/Local
import private

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
            cell = "".join(str(input("Please type in cell_id to print box label for: ")).split())
            qty = "".join(str(input("Please type in the QUANTITY of cells in the box:  ")).split())

            cell_list = sparc.select(
                rf"""select workorder, 'N/A' as batch, p.partnumber, location
                from sparc.thing t
                inner join sparc.part p on p.id = t.partid
                where CONCAT(p.partnumber,':',t.thingname) like '{cell}'
                or t.thingname like '{cell}'
                group by workorder, p.partnumber, location"""
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
                z.send(
                    host=os.getenv("zt421_host", private.zt421_host), port=os.getenv("zt421_port", private.zt421_port)
                )

    except Exception as E:
        print(E, type(E).__name__, __file__, E.__traceback__.tb_lineno)
