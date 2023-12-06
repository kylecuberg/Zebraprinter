# Standard library
from os import getenv

# Third-party
import util

# First-party/Local
import private

if __name__ == "__main__":
    """[summary]"""

    try:
        # get from sql
        sparc = util.MySQL(
            getenv("mysql_user", private.mysql_user),
            getenv("mysql_password", private.mysql_password),
            getenv("mysql_host", private.mysql_host),
            database=getenv("mysql_database", "sparc"),
        )

        while True:
            cell = "".join(str(input("Please type in cell_id to print box label for: ")).split())
            cell_no_pn = cell.split(":", 1)[1]
            print(cell, "", cell_no_pn)
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
                where i.barcode like '%{cell}'
                group by i.lot, i.cellformat, i.location, r.batch"""
            ).values.tolist()

            for row in cell_list:
                lot = row[0]
                batch = row[1]
                cellformat = row[2]
                celllocation = row[3]

                label = util.qr_text(dpi=300, label_x=3, label_y=2)
                z = util.zebra(qr=label.boxlabel(lot, batch, cellformat, celllocation))
                z.send(host=getenv("zt421_host", private.zt421_host), port=getenv("zt421_port", private.zt421_port))

    except Exception as E:
        print(E, type(E).__name__, __file__, E.__traceback__.tb_lineno)
