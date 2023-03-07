# Changelog

2023_03_07
    Attempt to standardize installation procedures & use more dynamic referencing for additional computers

2023_03_06
    Added processboxlabel functions, improved util

2023_01_25
    Added second printer lookup for ZT421

2022_10_10
    Added input check function

## For equipment labels

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

## Small barcodes

"""^XA
^FO0,0,0
^BQN,2,2,Q,7
^FDQA, {qr} ^FS
^CF0,15,15
^FO55,20^FD{qr}^FS
^XZ"""

## intermediate barcodes

r"""^XA
^FO150,0,0^FB 400,2, 10, C
^BQN,2,5,Q,7
^FDQA,{sn}^FS
^CF0,30,30
^FO0,120,0,C^FB 400, 2, 10, C^FH^FD{sn}\&{raw}^FS
^XZ"""

## ZPL A5 labels

"""^XA
        ^FX Outline box
        ^FO0,0^GB1680,1180,2^FS
        ^FX individual boxes
        ^FO0,0^GB840,161,1^FS
        ^FO0,0^GB1680,161,1^FS
        ^FO0,160^GB840,201,1^FS
        ^FO840,160^GB840,101,1^FS
        ^FO840,260^GB281,101,1^FS
        ^FO1120,260^GB280,101,1^FS
        ^FO1400,260^GB280,101,1^FS
        ^FO0,360^GB1121,241,1^FS
        ^FO1120,360^GB560,241,1^FS
        ^FO0,600^GB840,221,1^FS
        ^FO840,600^GB840,81,1^FS
        ^FO840,680^GB840,221,1^FS
        ^FO0,820^GB840,161,1^FS
        ^FO840,900^GB421,81,1^FS
        ^FO1260,900^GB420,81,1^FS
        ^FO0,980^GB840,201,1^FS
        ^FO840,980^GB840,201,1^FS

        ^FX Labels
        ^CFA,12,7
        ^FO30,30^FD(1) Reciever^FS
        ^FO870,30^FD(2) Delivery Location^FS
        ^FO30,170^FD(3) Advice Note (N)^FS
        ^FO850,170^FD(4) Supplier Address^FS
        ^FO850,270^FD(5) Net Wt^FS
        ^FO1130,270^FD(6) Gross Wt^FS
        ^FO1410,270^FD(7) No Boxes^FS
        ^FO30,370^FD(8) Part Number^FS
        ^FO30,610^FD(9) Quantity (Q)^FS
        ^FO850,610^FD(10) Description^FS
        ^FO850,690^FD(11) Supplier Part No (30S)^FS
        ^FO30,830^FD(12) Supplier (V)^FS
        ^FO850,910^FD(13) Date^FS
        ^FO1270,910^FD(14) Engineering Revision^FS
        ^FO30,990^FD(15) Serial No (S)^FS
        ^FO850,990^FD(16) Batch No (H)^FS
        ^FO30,1160^FD(17) 2020 Williams St Suite E, San Leandro CA 94677^FS

        ^FX Text
        ^CF0,30,30
        ^FO30,50^FD{label.get("Address1")}^FS
        ^FO30,90^FD{label.get("Address2")}^FS
        ^FO30,130^FD{label.get("Address3")}^FS
        ^FO30,240 ^A00,30,30 ^BCN,70,Y,Y ^FD{label.get("PO")}^FS
        ^FO850,190^FD2020 Williams St Suite E, San Leandro CA 94677^FS
        ^FO850,300^FD{label.get("Net")}^FS
        ^FO1130,300^FD{label.get("Gross")}^FS
        ^FO1420,300^FD{label.get("Boxes")}^FS
        ^FO30,440 ^A00,30,30 ^BCN,70,Y,Y ^FD{label.get("PN")}^FS
        ^FO30,680 ^A00,30,30 ^BCN,70,Y,Y ^FD{label.get("Quantity")}^FS
        ^FO860,640^FDLi-Metal Battery^FS
        ^FO860,750 ^A00,30,30 ^BCN,70,Y,Y ^FD{label.get("Supplier_PN")}^FS
        ^FO30,900 ^A00,30,30 ^BCN,70,Y,Y ^FD{label.get("SupplierNumber")}^FS
        ^FO860,940^FDDD.MM.YYYY^FS
        ^FO1280,940^FD{label.get("Revision")}^FS
        ^FO30,1050 ^A00,30,30 ^BCN,70,Y,Y ^FD{label.get("Serial")}^FS
        ^FO860,1050 ^A00,30,30 ^BCN,70,Y,Y ^FD{label.get("Batch")}^FS
        ^XZ"""
