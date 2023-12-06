# Third-party
import PySimpleGUI as sg

# First-party/Local
from generalized_cell import generalized_barcode_generation
from private import zt421_dpi, zt421_host, zt421_port

# Validations
# Production Boxes -> Works for 751015:SLV2231205001
# Process Boxes -> None
# Cell -> Only checked cage print
# EL -> All 4 buttons checked


class combined_gui:
    def __init__(self, theme="Dark"):
        sg.theme(theme)
        self.main_window = sg.Window(
            "Label Printing",
            [
                [sg.Text("Select the type of printing you wish to do")],
                [sg.Button("Production boxes"), sg.Button("Process boxes"), sg.Button("Cell"), sg.Button("EL")],
            ],
        )
        while True:
            event, values = self.main_window.read()
            if event == "Exit" or event == sg.WIN_CLOSED:
                break
            elif event == "Production boxes":
                self._production_boxes()
            elif event == "Process boxes":
                self._process_boxes()
            elif event == "Cell":
                self._cell()
            elif event == "EL":
                self._el()
        self.main_window.close()

    def _cell(self):
        self._cell_window = sg.Window(
            "Cell Layout",
            [
                [sg.Text("Enter text to print")],
                [sg.Text("Text", size=(20, 2)), sg.InputText(do_not_clear=False)],
                [sg.Button("Dryroom Print"), sg.Button("Cage Print")],
            ],
        )
        gbg = generalized_barcode_generation()
        while True:
            try:
                event, values = self._cell_window.read()
                print(event, values)
                if event == "Exit" or event == sg.WIN_CLOSED:
                    break
                elif event == "Dryroom Print":
                    gbg.entered(check_override=True, value=values[0])
                    gbg.send(printer_name="ZDesigner ZT411R-203dpi ZPL", conn_type="name")
                elif event == "Cage Print":
                    gbg.entered(value=values[0])
                    gbg.send()
            except Exception as E:
                print(E, type(E).__name__, __file__, E.__traceback__.tb_lineno)
                break
        self._cell_window.close()
        self._cell_window = None

    def _production_boxes(self):
        self._box_window = sg.Window(
            "Box Layout",
            [
                [sg.Text("Please type in cell_id to print box label for: ")],
                [sg.Text("Text", size=(20, 2)), sg.InputText(do_not_clear=False)],
                [sg.Button("Print Label")],
                [sg.Text("*Note, cell_id must be in 'PN:SN' format!")],
            ],
        )
        gbg = generalized_barcode_generation()
        while True:
            try:
                event, values = self._box_window.read()
                print(event, values)
                if event == "Exit" or event == sg.WIN_CLOSED:
                    break
                elif event == "Print Label":
                    gbg.productionboxlabel(values[0])
                    gbg.send(host=zt421_host, port=zt421_port, dpi=zt421_dpi)
                    gbg.reset()
            except Exception as E:
                print(E, type(E).__name__, __file__, E.__traceback__.tb_lineno)
                break
        self._box_window.close()
        self._box_window = None

    def _process_boxes(self):
        self._box_window = sg.Window(
            "Box Layout",
            [
                [
                    sg.Text("Please type in cell_id to print box label for: ", size=(20, 2)),
                    sg.InputText(do_not_clear=False),
                ],
                [
                    sg.Text("Please type in QUANTITY to print box label for: ", size=(20, 2)),
                    sg.InputText(do_not_clear=False),
                ],
                [sg.Button("Print Label")],
                [sg.Text("*Note, cell_id must be in 'PN:SN' format!")],
            ],
        )
        gbg = generalized_barcode_generation()
        while True:
            try:
                event, values = self._box_window.read()
                print(event, values)
                if event == "Exit" or event == sg.WIN_CLOSED:
                    break
                elif event == "Print Label":
                    gbg.processboxlabel(values[0], values[1])
                    gbg.send(host=zt421_host, port=zt421_port, dpi=zt421_dpi)
                    gbg.reset()
            except Exception as E:
                print(E, type(E).__name__, __file__, E.__traceback__.tb_lineno)
                break
        self._box_window.close()
        self._box_window = None

    def _el(self):
        self._el_window = sg.Window(
            "EL Layout",
            [
                [sg.Text("Pick the Option to print")],
                [sg.Button("Set 1"), sg.Button("Set 2"), sg.Button("Set 3"), sg.Button("Text")],
                [sg.Text("Text", size=(20, 2)), sg.InputText(do_not_clear=False)],
            ],
        )
        gbg = generalized_barcode_generation()
        qr = ""
        while True:
            try:
                event, values = self._el_window.read()
                print(event, values)
                if event == "Exit" or event == sg.WIN_CLOSED:
                    break
                elif event == "Set 1":
                    qr = r"""^XA
                    ^CF0,25,25^FO10,20,0^FDSolvent 1^FS
                    ^CF0,25,25^FO10,75,0^FDSolvent 2^FS
                    ^CF0,25,25^FO10,135,0^FDSolvent 4^FS
                    ^XZ"""
                elif event == "Set 2":
                    qr = r"""^XA
                    ^CF0,25,25^FO10,20,0^FDSolvent 7^FS
                    ^CF0,25,25^FO10,75,0^FDDiluent 2^FS
                    ^CF0,25,25^FO10,135,0^FDSalt 1^FS
                    ^XZ"""
                elif event == "Set 3":
                    qr = r"""^XA
                    ^CF0,25,25^FO10,20,0^FDSalt 4^FS
                    ^CF0,25,25^FO10,75,0^FDMixer EL^FS
                    ^CF0,25,25^FO10,135,0^FDVessel EL^FS
                    ^XZ"""
                else:
                    qr = f"""^XA
                    ^CF0,25,25^FO10,75,0^FD{values[0]}^FS
                    ^XZ"""
                gbg.send(qr=qr)
                gbg.reset()
            except Exception as E:
                print(E, type(E).__name__, __file__, E.__traceback__.tb_lineno)
                break
        self._el_window.close()
        self._el_window = None


def main():
    combined_gui()


if __name__ == "__main__":
    main()
