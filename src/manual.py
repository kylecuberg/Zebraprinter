# First-party/Local
import util

if __name__ == "__main__":
    """[summary]"""

    cell_list = util.loop_xlsb_file(
        r"""C:\Users\KylePatterson\Documents\CubergGithub\zebraPrinter\input\Print_File.xlsb""", columns=2
    )

    try:
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
