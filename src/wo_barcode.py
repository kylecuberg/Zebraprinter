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

        wo_list = "".join(str(input("Please type in Work Order to print labels for: ")).strip())

        for wo in [wo_list]:
            wo = str(wo)
            cell_list = sparc.select(
                rf"""SELECT t.thingname, g.thingname FROM thing t
                         inner join genealogy g on t.thingname = g.parentthingname
                         where workorder like {wo} order by t.thingname desc"""
            ).values.tolist()

            for row in cell_list:
                cell = row[0]
                barcode = row[1]

                qr = f"""^XA^FO20,40,0^BQN,2,5,Q,7^FDQA,{cell}^FS
                ^CF0,40,32^FO160,90,0^FD{cell}^FS
                ^CF0,20,20^FO160,170,0^FDRaw-{barcode}^FS
                ^XZ"""
                z = util.zebra(qr=qr)
                z.send()

                label = util.qr_text(label_x=2, label_y=1, dpi=os.getenv("zt411_dpi", private.zt411_dpi))
                z = util.zebra(qr=label.sn(cell=cell, barcode=barcode))
                z.send(
                    host=os.get_env("zt411_host", private.zt411_host), port=os.get_env("zt411_port", private.zt411_port)
                )
    except Exception as E:
        print(E, type(E).__name__, __file__, E.__traceback__.tb_lineno)
