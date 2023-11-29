# First-party/Local
import generalized_cell

if __name__ == "__main__":
    """[summary]"""
    try:
        gbg = generalized_cell.generalized_barcode_generation()
        while True:
            gbg.manual()
            gbg.send()
            gbg.reset()
    except Exception as E:
        print(E, type(E).__name__, __file__, E.__traceback__.tb_lineno)
