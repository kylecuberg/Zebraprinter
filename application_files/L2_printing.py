# First-party/Local
import generalized_cell

if __name__ == "__main__":
    """[summary]"""
    try:
        gbg = generalized_cell.generalized_barcode_generation()
        while True:
            gbg.entered(check_override=True, string_override="Type in what to print: ")
            gbg.send(printer_name="ZDesigner ZT411R-203dpi ZPL", conn_type="name")  # qr_loc="20,20", cell_loc="150,20"
            gbg.reset()
    except Exception as E:
        print(E, type(E).__name__, __file__, E.__traceback__.tb_lineno)
        input("Press Enter to close")
