# Third-party
import PySimpleGUI as sg

# First-party/Local
import generalized_cell

"""
https://dzone.com/articles/pysimplegui-working-with-multiple-windows

https://www.blog.pythonlibrary.org/2021/01/20/pysimplegui-working-with-multiple-windows/
"""


class combined_gui:
    def __init__(self, theme="Dark"):
        sg.theme(theme)
        self.main_window = sg.Window(
            "Label Printing",
            [
                [sg.Text("Select the type of printing you wish to do")],
                [sg.Button("Boxes"), sg.Button("Cell"), sg.Button("EL")],
            ],
        )
        while True:
            event, values = self.main_window.read()
            if event == "Exit" or event == sg.WIN_CLOSED:
                break
            elif event == "Boxes":
                self._boxes()
            elif event == "Cell":
                self._cell()
            elif event == "EL":
                self._el()
        self.main_window.close()

    def _boxes(self):
        self._box_window = sg.Window(
            "Box Layout",
            [
                [sg.Text("Enter text to print")],
                [sg.Text("Text", size=(20, 2)), sg.InputText(do_not_clear=False)],
                [sg.Button("box"), sg.Button("process box")],
            ],
        )
        while True:
            event, values = self._box_window.read()
            print(event, values)
            if event == "Exit" or event == sg.WIN_CLOSED:
                break
        self._box_window.close()
        self._box_window = None

    def _cell(self):
        self._cell_window = sg.Window(
            "Cell Layout",
            [
                [sg.Text("Enter text to print")],
                [sg.Text("Text", size=(20, 2)), sg.InputText(do_not_clear=False)],
                [sg.Button("Print Dryroom"), sg.Button("Print Cage")],
            ],
        )
        while True:
            event, values = self._cell_window.read()
            print(event, values)
            if event == "Exit" or event == sg.WIN_CLOSED:
                break
        self._cell_window.close()
        self._cell_window = None

    def _el(self):
        self._el_window = sg.Window(
            "EL Layout",
            [
                [sg.Text("Enter text to print")],
                [sg.Text("Text", size=(20, 2)), sg.InputText(do_not_clear=False)],
                [sg.Button("EL")],
            ],
        )
        while True:
            event, values = self._el_window.read()
            print(event, values)
            if event == "Exit" or event == sg.WIN_CLOSED:
                break
        self._el_window.close()
        self._el_window = None


class label_gui:
    def __init__(self, text, theme="Dark"):
        sg.theme(theme)
        self.window = sg.Window("Cell Label Printing", self.layout)

    def get_data(self):
        try:
            event, values = self.window.read()
        except Exception as E:
            print(E, type(E).__name__, __file__, E.__traceback__.tb_lineno)
        return event, values


def old():
    try:
        a = label_gui("Enter text to print")
        gbg = generalized_cell.generalized_barcode_generation()
        while True:
            event, values = a.get_data()
            if event == sg.WIN_CLOSED:
                break
            elif event == "Dryroom Print":
                gbg.entered(check_override=True, value=values[0])
                gbg.send(printer_name="ZDesigner ZT411R-203dpi ZPL", conn_type="name")
            elif event == "Cage Print":
                gbg.entered(value=values[0])
                gbg.send()
            gbg.reset()
    except Exception as E:
        print(E, type(E).__name__, __file__, E.__traceback__.tb_lineno)


def main():
    combined_gui()


if __name__ == "__main__":
    main()
