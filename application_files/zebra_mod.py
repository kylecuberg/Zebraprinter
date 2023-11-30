# Third-party
from zebra import Zebra

qr1 = r"""^XA
    ^CF0,25,25^FO10,20,0^FDSolvent 1^FS
    ^XZ"""
try:
    z = Zebra()
    z.setqueue("ZDesigner ZT411R-203dpi ZPL")
    z.output(qr1)
except Exception as E:
    print(E, type(E).__name__, __file__, E.__traceback__.tb_lineno)

input("Press Enter to close")
