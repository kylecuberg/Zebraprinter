# First-party/Local
import util

if __name__ == "__main__":
    """[summary]"""
    val_list = [
        "SL-FM1-NF1-1-1-1",
        "SL-FM1-NF1-1-1-2",
        "SL-FM1-NF1-1-1-3",
        "SL-FM1-NF1-1-1-4",
        "SL-FM1-NF1-1-1-5",
        "SL-FM1-NF1-1-1-6",
        "SL-FM1-NF1-1-1-7",
        "SL-FM1-NF1-1-1-8",
        "SL-FM1-NF1-1-2-1",
        "SL-FM1-NF1-1-2-2",
        "SL-FM1-NF1-1-2-3",
        "SL-FM1-NF1-1-2-4",
        "SL-FM1-NF1-1-2-5",
        "SL-FM1-NF1-1-2-6",
        "SL-FM1-NF1-1-2-7",
        "SL-FM1-NF1-1-2-8",
        "SL-FM1-NF1-2-1-1",
        "SL-FM1-NF1-2-1-2",
        "SL-FM1-NF1-2-1-3",
        "SL-FM1-NF1-2-1-4",
        "SL-FM1-NF1-2-1-5",
        "SL-FM1-NF1-2-1-6",
        "SL-FM1-NF1-2-1-7",
        "SL-FM1-NF1-2-1-8",
        "SL-FM1-NF1-2-2-1",
        "SL-FM1-NF1-2-2-2",
        "SL-FM1-NF1-2-2-3",
        "SL-FM1-NF1-2-2-4",
        "SL-FM1-NF1-2-2-5",
        "SL-FM1-NF1-2-2-6",
        "SL-FM1-NF1-2-2-7",
        "SL-FM1-NF1-2-2-8",
        "SL-FM1-NF1-3-1-1",
        "SL-FM1-NF1-3-1-2",
        "SL-FM1-NF1-3-1-3",
        "SL-FM1-NF1-3-1-4",
        "SL-FM1-NF1-3-1-5",
        "SL-FM1-NF1-3-1-6",
        "SL-FM1-NF1-3-1-7",
        "SL-FM1-NF1-3-1-8",
        "SL-FM1-NF1-3-2-1",
        "SL-FM1-NF1-3-2-2",
        "SL-FM1-NF1-3-2-3",
        "SL-FM1-NF1-3-2-4",
        "SL-FM1-NF1-3-2-5",
        "SL-FM1-NF1-3-2-6",
        "SL-FM1-NF1-3-2-7",
        "SL-FM1-NF1-3-2-8",
        "SL-FM1-NF1-4-1-1",
        "SL-FM1-NF1-4-1-2",
        "SL-FM1-NF1-4-1-3",
        "SL-FM1-NF1-4-1-4",
        "SL-FM1-NF1-4-1-5",
        "SL-FM1-NF1-4-1-6",
        "SL-FM1-NF1-4-1-7",
        "SL-FM1-NF1-4-1-8",
        "SL-FM1-NF1-4-2-1",
        "SL-FM1-NF1-4-2-2",
        "SL-FM1-NF1-4-2-3",
        "SL-FM1-NF1-4-2-4",
        "SL-FM1-NF1-4-2-5",
        "SL-FM1-NF1-4-2-6",
        "SL-FM1-NF1-4-2-7",
        "SL-FM1-NF1-4-2-8",
    ]

    for val in val_list:
        qr = rf"""^XA
        ^FO50,35^BQN,2,4,H,6^FDQA,{str(val)}^FS
        ^CF0,20,20^FO150,75,0^FD{str(val)}^FS^XZ
        """
        z = util.zebra(qr=qr)
        z.send()
