# Standard library
import os

# First-party/Local
import private
import util

if __name__ == "__main__":
    """[summary]"""

    cell_list = util.loop_xlsb_file(
        os.path.abspath(os.path.join(os.pardir(), "input", "Print_File.xlsb")),
        columns=2,
    )

    try:
        for row in cell_list:
            cell = row[0]
            barcode = row[1]

            label = util.qr_text(label_x=2, label_y=1, dpi=os.getenv("zt411_dpi", private.zt411_dpi))
            z = util.zebra(qr=label.sn_barcode(cell=cell, barcode=barcode))
            z.send(host=os.getenv("zt411_host", private.zt411_host), port=os.getenv("zt411_port", private.zt411_port))

    except Exception as E:
        print(E, type(E).__name__, __file__, E.__traceback__.tb_lineno)
