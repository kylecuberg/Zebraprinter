# Standard library
import os

# First-party/Local
import private
import util

if __name__ == "__main__":
    """[summary]"""

    cell_list = util.loop_xlsb_file(
        r"""C:\Users\KylePatterson\Documents\CubergGithub\zebraPrinter\input\Print_File.xlsb"""
    )

    try:
        # get from sql
        sparc = util.MySQL(
            os.getenv("mysql_user", private.mysql_user),
            os.getenv("mysql_password", private.mysql_password),
            os.getenv("mysql_host", private.mysql_host),
            database=os.getenv("mysql_database", "sparc"),
        )

        for cell in cell_list:
            cell = str(cell[0])
            cell_list = sparc.select(
                rf"""SELECT t.thingname, g.thingname FROM thing t
                         inner join genealogy g on t.thingname = g.parentthingname
                         where t.thingname like '{cell}' order by t.thingname desc"""
            ).values.tolist()

            for row in cell_list:
                cell = row[0]
                barcode = row[1]

                qr = f"""^XA^FO20,40,0^BQN,2,5,Q,7^FDQA,{cell}^FS
                ^CF0,40,32^FO140,90,0^FD{cell}^FS
                ^CF0,20,20^FO140,170,0^FDRaw-{barcode}^FS
                ^XZ"""
                z = util.zebra(qr=qr)
                z.send()

    except Exception as E:
        print(E, type(E).__name__, __file__, E.__traceback__.tb_lineno)
