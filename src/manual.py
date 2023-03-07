# Standard library
import os

# First-party/Local
import private
import util

if __name__ == "__main__":
    """[summary]"""

    cell_list = util.loop_xlsb_file(
        # r"""C:\Users\KylePatterson\Documents\CubergGithub\zebraPrinter\input\Print_File.xlsb""", columns=2
        os.path.abspath(os.path.join(os.pardir(), r"\input\Print_File.xlsb")),
        columns=2,
    )

    try:
        for row in cell_list:
            cell = row[0]
            barcode = row[1]

            label = util.qr_text(dpi=203)
            z = util.zebra(qr=label.sn(cell=cell, barcode=barcode))
            z.send(host=os.get_env("zt411_host", private.zt411_host), port=os.get_env("zt411_port", private.zt411_port))

    except Exception as E:
        print(E, type(E).__name__, __file__, E.__traceback__.tb_lineno)
