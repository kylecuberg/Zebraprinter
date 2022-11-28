# First-party/Local
import util

if __name__ == "__main__":
    """[summary]"""

    cell_list = util.loop_xlsb_file(
        r"""C:\Users\KylePatterson\Documents\CubergGithub\zebraPrinter\input\Print_File.xlsb"""
    )

    for cell in cell_list:
        qr = f"""^XA
        ^FO150,10,2
        ^BQN,2,5,Q,7
        ^FDQA, {cell} ^FS
        ^CF0,30,30
        ^FO165,160,2^FD{cell}^FS
        ^XZ"""
        z = util.zebra(qr=qr)
        z.send()
