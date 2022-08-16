# Standard library
import os
import socket


def zebraPrintSN(sn="serial", raw="raw"):
    # Main function
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((os.getenv("ops_host"), int(os.getenv("ops_port"))))
            txt = rf"""^XA
                ^FO170,10,2^FB 400,2, 10, C
                ^BQN,2,4,Q,7
                ^FDQA,{sn}^FS
                ^CF0,30,30
                ^FO10,125^FB 400, 2, 10, C^FH^FD{sn}\&{raw}^FS
                ^XZ"""
            sock.send(bytes(txt, "utf-8"))  # using bytes
    except Exception as E:
        print(type(E).__name__, __file__, E.__traceback__.tb_lineno, "\n", E)


if __name__ == "__main__":
    """[summary]"""
    zebraPrintSN(sn="SLEV220809127", raw="2209004100071")

# For equipment labels
"""^XA
                      ^FO0,0,0
                      ^BQN,2,6,Q,7
                      ^FDQA,3MXWLQKV42JA^FS
                      ^CF0,40,40
                      ^FO155,10^FD[CNC1-1]^FS
                      ^CF0,40,40
                      ^FO155,50^FDCNC Machine^FS
                      ^CF0,20,20
                      ^FO0,150^FD3MXWLQKV42JA^FS
                      ^XZ"""

# Small barcodes
"""^XA
        ^FO0,0
        ,0
        ^BQN,2,2,Q,7
        ^FDQA, {sn} ^FS
        ^CF0,15,15
        ^FO55,10^FD{raw}^FS
        ^CF0,15,15
        ^FO55,40^FD{sn}^FS
        ^XZ"""

# intermediate barcodes
r"""^XA
        ^FO150,0,0^FB 400,2, 10, C
        ^BQN,2,5,Q,7
        ^FDQA,{sn}^FS
        ^CF0,30,30
        ^FO0,120,0,C^FB 400, 2, 10, C^FH^FD{sn}\&{raw}^FS
        ^XZ"""
