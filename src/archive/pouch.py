# Standard library
from datetime import date

# Third-party
import util


def get_info():
    while True:
        info = str(input("Type in 1 (V1 Poucher) or 2 (V2 Poucher): "))
        if info == "1":
            return "PCH1-1"
        elif info == "2":
            return "PCH2-1"


if __name__ == "__main__":
    """[summary]"""

    try:
        pn = "3mm251"
        d1 = date.today().strftime(r"%y%m%d")
        equip = get_info()
        pouch = f"{pn}:{equip}:{d1}"

        qr = f"""^XA^FO20,40,0^BQN,2,5,Q,7^FDQA,{pouch}^FS
                ^CF0,40,32^FO140,90,0^FD{pouch}^FS
                ^XZ"""
        z = util.zebra(qr=qr)
        # z.send()
        print(pouch)

    except Exception as E:
        print(E, type(E).__name__, __file__, E.__traceback__.tb_lineno)
