# Standard library
import os
import socket


def zebraPrintSN(qr=""):
    # Main function
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((os.getenv("ops_host"), int(os.getenv("ops_port"))))
            txt = rf"""^XA
            ^FO0,0,0
            ^BQN,2,2,Q,7
            ^FDQA, {qr} ^FS
            ^CF0,15,15
            ^FO55,20^FD{qr}^FS
            ^XZ"""
            sock.send(bytes(txt, "utf-8"))  # using bytes
    except Exception as E:
        print(type(E).__name__, __file__, E.__traceback__.tb_lineno, "\n", E)


def get_input():
    a = input("Please enter PN: ")
    if a.startswith("P"):
        a = a[1:]

    while True:
        b = input("Please enter Serial Number:")
        if b.startswith("SLV"):
            b = b
            break
    # P700009:SLV1100509
    c = f"P{a}:{b}"
    print(c)
    return c


if __name__ == "__main__":
    """[summary]"""
    zebraPrintSN(sn=get_input())
