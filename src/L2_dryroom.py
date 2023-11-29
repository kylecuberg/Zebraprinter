# First-party/Local
import generalized_cell

if __name__ == "__main__":
    """[summary]"""
    try:
        gbg = generalized_cell.generalized_barcode_generation(printer="l2")
        while True:
            gbg.manual(check_override=True, string_override="Type in what to print: ")
            gbg.send()
            gbg.reset()
    except Exception as E:
        print(E, type(E).__name__, __file__, E.__traceback__.tb_lineno)
