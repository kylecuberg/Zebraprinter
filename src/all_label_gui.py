# Third-party
import pkg_resources
from PySimpleGUI import WIN_CLOSED, Button, InputText, Multiline, Text, Window
from PySimpleGUI import theme as sgtheme

# First-party/Local
from private import zt421_dpi, zt421_host, zt421_port
from util import generalized_barcode_generation


class combined_gui:
    def __init__(self, theme="Dark"):
        sgtheme(theme)
        self.main_window = Window(
            "Label Printing",
            [
                [Text("Select the type of printing you wish to do")],
                [
                    Button("Production boxes"),
                    Button("Process boxes"),
                    Button("Cage"),
                    Button("Dryroom"),
                    Button("EL"),
                    Button("Custom"),
                ],
                [Text("Version " + str(__version__))],
            ],
        )
        while True:
            event, values = self.main_window.read()
            if event == "Exit" or event == WIN_CLOSED:
                break
            elif event == "Production boxes":
                self._production_boxes()
            elif event == "Process boxes":
                self._process_boxes()
            elif event == "Cage":
                self._cage()
            elif event == "Dryroom":
                self._custom(printer_name="ZDesigner ZT411R-203dpi ZPL", conn_type="name")
            elif event == "EL":
                self._el()
            elif event == "Custom":
                self._custom()
        self.main_window.close()

    def _cage(self):
        self._cell_window = Window(
            "Cell Layout",
            [
                [Text("Cell/Barcode/WO", size=(20, 2)), InputText(do_not_clear=False, key="-Input-")],
                [Button("Print", bind_return_key=True)],
            ],
        )
        gbg = generalized_barcode_generation()
        while True:
            try:
                event, values = self._cell_window.read()
                print(event, values)
                if event == "Exit" or event == WIN_CLOSED:
                    break
                elif event == "Print":
                    gbg.entered(value=values["-Input-"])
                    gbg.send()
                    gbg.reset()
            except Exception as E:
                print(E, type(E).__name__, __file__, E.__traceback__.tb_lineno)
                # break
        self._cell_window.close()
        self._cell_window = None

    def _production_boxes(self):
        self._box_window = Window(
            "Box Layout",
            [
                [Text("Please type in cell_id to print box label for: ")],
                [Text("Text", size=(20, 2)), InputText(do_not_clear=False, key="-Input-")],
                [Button("Print Label", bind_return_key=True)],
                [Text("*Note, cell_id must be in 'PN:SN' format!")],
            ],
        )
        gbg = generalized_barcode_generation()
        while True:
            try:
                event, values = self._box_window.read()
                print(event, values)
                if event == "Exit" or event == WIN_CLOSED:
                    break
                elif event == "Print Label":
                    gbg.productionboxlabel(values["-Input-"])
                    gbg.send(host=zt421_host, port=zt421_port, dpi=zt421_dpi)
                    gbg.reset()
            except Exception as E:
                print(E, type(E).__name__, __file__, E.__traceback__.tb_lineno)
                break
        self._box_window.close()
        self._box_window = None

    def _process_boxes(self):
        self._box_window = Window(
            "Box Layout",
            [
                [
                    Text("Please type in cell_id to print box label for: ", size=(20, 2)),
                    InputText(do_not_clear=False, key="cell_id"),
                ],
                [
                    Text("Please type in QUANTITY to print box label for: ", size=(20, 2)),
                    InputText(do_not_clear=False, key="QTY"),
                ],
                [Button("Print Label")],
                [Text("*Note, cell_id must be in 'PN:SN' format!")],
            ],
        )
        gbg = generalized_barcode_generation()
        while True:
            try:
                event, values = self._box_window.read()
                print(event, values)
                if event == "Exit" or event == WIN_CLOSED:
                    break
                elif event == "Print Label":
                    gbg.processboxlabel(values["cell_id"], values["QTY"])
                    gbg.send(host=zt421_host, port=zt421_port, dpi=zt421_dpi)
                    gbg.reset()
            except Exception as E:
                print(E, type(E).__name__, __file__, E.__traceback__.tb_lineno)
                break
        self._box_window.close()
        self._box_window = None

    def _el(self):
        self._el_window = Window(
            "EL Layout",
            [
                [Text("Pick the Option to print")],
                [Button("Set 1"), Button("Set 2"), Button("Set 3"), Button("Text")],
                [Text("Text", size=(20, 2)), InputText(do_not_clear=False)],
            ],
        )
        gbg = generalized_barcode_generation()
        qr = ""
        while True:
            try:
                event, values = self._el_window.read()
                print(event, values)
                if event == "Exit" or event == WIN_CLOSED:
                    break
                elif event == "Set 1":
                    qr = r"""^XA
                    ^CF0,25,25^FO25,20,0^FDSolvent 1^FS
                    ^CF0,25,25^FO25,75,0^FDSolvent 2^FS
                    ^CF0,25,25^FO25,135,0^FDSolvent 4^FS
                    ^XZ"""
                elif event == "Set 2":
                    qr = r"""^XA
                    ^CF0,25,25^FO25,20,0^FDSolvent 7^FS
                    ^CF0,25,25^FO25,75,0^FDDiluent 2^FS
                    ^CF0,25,25^FO25,135,0^FDSalt 1^FS
                    ^XZ"""
                elif event == "Set 3":
                    qr = r"""^XA
                    ^CF0,25,25^FO25,20,0^FDSalt 4^FS
                    ^CF0,25,25^FO25,75,0^FDMixer EL^FS
                    ^CF0,25,25^FO25,135,0^FDVessel EL^FS
                    ^XZ"""
                else:
                    qr = f"""^XA
                    ^CF0,25,25^FO25,75,0^FD{values[0]}^FS
                    ^XZ"""
                gbg.send(qr=qr)
                gbg.reset()
            except Exception as E:
                print(E, type(E).__name__, __file__, E.__traceback__.tb_lineno)
                break
        self._el_window.close()
        self._el_window = None

    def _custom(self, **kwargs):
        self._custom_window = Window(
            "CustomPrinting",
            [
                [
                    Multiline(
                        "PrintMe",
                        size=(50, 10),
                        enter_submits=True,
                        expand_x=True,
                        expand_y=True,
                        do_not_clear=False,
                        key="-Input-",
                    )
                ],
                [Text("Settings for print [Default]-> ")],
                [
                    Text("TextSize [25]"),
                    InputText("25", 2, key="TextSize"),
                    Text("QRSize [4]"),
                    InputText("4", 2, key="QRSize"),
                ],
                [Button("Print")],
            ],
        )
        gbg = generalized_barcode_generation()
        qr = ""
        while True:
            try:
                event, values = self._el_window.read()
                print(event, values)
                if event == "Exit" or event == WIN_CLOSED:
                    break
                else:
                    None
                    if values["-Input-"].startswith("^XA") and values[0].endswith("^XZ"):
                        qr = values["-Input-"]
                        gbg.send(qr=qr)
                    elif kwargs.get("printer_name", False):
                        gbg.entered(check_override=True, value=values["-Input-"])
                        gbg.send(
                            printer_name=kwargs.get("printer_name", "ZDesigner ZT411R-203dpi ZPL"),
                            conn_type=kwargs.get("conn_type", "name"),
                        )
                    else:
                        qr = rf"""^XA
                        ^FO30,30^BQN,2,{values['QRSize']},H,6^FDQA,{values["-Input-"]}^FS
                        ^CF0,{values['TextSize']},{values['TextSize']}^FO175,75,0^FB225,5,0,L,0^FD{values["-Input-"]}^FS^XZ"""
                        gbg.send(qr=qr)
                    gbg.reset()
            except Exception as E:
                print(E, type(E).__name__, __file__, E.__traceback__.tb_lineno)
                break
        self._custom_window.close()
        self._custom_window = None


def main():
    combined_gui()


if __name__ == "__main__":
    __version__ = pkg_resources.get_distribution("ZebraPrinter").version
    main()
