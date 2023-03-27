# Standard library
import os

# First-party/Local
import private
import util

if __name__ == "__main__":
    """[summary]"""

    cell_list = util.loop_xlsb_file(os.path.abspath(os.path.join(os.pardir(), "input", "Print_File.xlsb")), columns=1)

    try:
        # get from sql
        sparc = util.MySQL(
            os.getenv("mysql_user", private.mysql_user),
            os.getenv("mysql_password", private.mysql_password),
            os.getenv("mysql_host", private.mysql_host),
            database=os.getenv("mysql_database", "sparc"),
        )

        for cell in cell_list:
            cell_items = sparc.select(
                rf"""select t.thingname, t.workorder, CASE WHEN g.thingname like 'CHG%' THEN '' ELSE g.thingname END AS raw
                from sparc.thing t
                left join sparc.genealogy g on g.parentthingname = t.thingname
                where t.thingname like '{cell}' order by t.thingname desc"""
            ).values.tolist()

            for row in cell_items:
                cell = row[0]
                workorder = row[1]
                barcode = row[2]

                label = util.qr_text(label_x=2, label_y=1, dpi=os.getenv("zt411_dpi", private.zt411_dpi))
                z = util.zebra(qr=label.sn_combo(cell=cell, workorder=workorder, barcode=barcode))
                z.send(
                    host=os.getenv("zt411_host", private.zt411_host), port=os.getenv("zt411_port", private.zt411_port)
                )

    except Exception as E:
        print(E, type(E).__name__, __file__, E.__traceback__.tb_lineno)
