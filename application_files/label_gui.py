# Third-party
import PySimpleGUI as sg

# First-party/Local
import generalized_cell


class label_gui:
    def __init__(self, text, theme="Dark"):
        sg.theme(theme)
        self.layout = [
            [sg.Text(text)],
            [sg.Text("Text", size=(20, 2)), sg.InputText(do_not_clear=False)],
            [sg.Button("Dryroom Print"), sg.Button("Cage Print")],
        ]
        self.window = sg.Window("Cell Label Printing", self.layout)

    def get_data(self):
        try:
            event, values = self.window.read()
        except Exception as E:
            print(E, type(E).__name__, __file__, E.__traceback__.tb_lineno)
        return event, values


def main():
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


if __name__ == "__main__":
    main()
