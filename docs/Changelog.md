# Changelog

2022_10_10
    Added input check function


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
^FO0,0,0
^BQN,2,2,Q,7
^FDQA, {qr} ^FS
^CF0,15,15
^FO55,20^FD{qr}^FS
^XZ"""

# intermediate barcodes
r"""^XA
^FO150,0,0^FB 400,2, 10, C
^BQN,2,5,Q,7
^FDQA,{sn}^FS
^CF0,30,30
^FO0,120,0,C^FB 400, 2, 10, C^FH^FD{sn}\&{raw}^FS
^XZ"""
