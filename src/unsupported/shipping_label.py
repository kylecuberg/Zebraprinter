# First-party/Local
import util


class shipping_label:
    def __init__(
        self,
        **kwargs,
    ):
        return None

    def _get_input(self, label_dict):
        for key in label_dict:
            label_dict[key] = str(input(f"Please enter the value for: {key}"))
        return label_dict

    def VDA4902(self):
        label_dict = {
            "Address1": "",
            "Address2": "",
            "Address3": "",
            "PO": "",
            "Net": "0",
            "Gross": "0",
            "Boxes": "0",
            "PN": "",
            "Quantity": "0",
            "Supplier_PN": "",
            "SupplierNumber": "0",
            "Revision": "",
            "Serial": "",
            "Batch": "",
        }

        label = self._get_input(label_dict)

        zpl = f"""^XA
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
        return zpl

    def UPS_Shipping(self):
        label_dict = {
            "Address1": "",
            "Address2": "",
            "Address3": "",
            "PO": "",
            "Net": "0",
            "Gross": "0",
            "Boxes": "0",
            "PN": "",
            "Quantity": "0",
            "Supplier_PN": "",
            "SupplierNumber": "0",
            "Revision": "",
            "Serial": "",
            "Batch": "",
        }

        label = self._get_input(label_dict)
        zpl = f"{label}"

        return zpl


if __name__ == "__main__":
    """[summary]"""

    qr = shipping_label.VDA4902()

    try:
        z = util.zebra(qr=qr)
        # z.send()

    except Exception as E:
        print(E, type(E).__name__, __file__, E.__traceback__.tb_lineno)
