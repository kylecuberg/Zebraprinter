# Standard library
from os import getenv

# Third-party
import util

# First-party/Local
import private

if __name__ == "__main__":
    """[summary]"""

    copies = 1

    qr1 = r"""^XA
    ^CF0,25,25^FO10,20,0^FDSolvent 1^FS
    ^CF0,25,25^FO10,75,0^FDSolvent 2^FS
    ^CF0,25,25^FO10,135,0^FDSolvent 4^FS
    ^XZ"""

    qr2 = r"""^XA
    ^CF0,25,25^FO10,20,0^FDSolvent 7^FS
    ^CF0,25,25^FO10,75,0^FDDiluent 2^FS
    ^CF0,25,25^FO10,135,0^FDSalt 1^FS
    ^XZ"""

    qr3 = r"""^XA
    ^CF0,25,25^FO10,20,0^FDSalt 4^FS
    ^CF0,25,25^FO10,75,0^FDMixer EL^FS
    ^CF0,25,25^FO10,135,0^FDVessel EL^FS
    ^XZ"""

    for qr in [qr1, qr2, qr3]:
        z = util.zebra(qr=qr)
        for ea in range(1, copies + 1):
            z.send(
                host=getenv("zt411_host", str(private.zt411_host)),
                port=getenv("zt411_port", str(private.zt411_port)),
            )
