# Standard library
import os
import socket


def main(sn="serial", raw="raw"):
    # Main function
    try:
        sock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
        sock.connect((os.getenv("zebramac"), 1))
        txt = f"""^XA
                      ^FO0,0,0
                      ^BQN,2,2,Q,7
                      ^FDQA, {sn} ^FS
                      ^CF0,15,15
                      ^FO55,10^FD{raw}^FS
                      ^CF0,15,15
                      ^FO55,40^FD{sn}^FS
                      ^XZ"""
        sock.send(bytes(txt, "utf-8"))  # using bytes
        sock.close()  # closing connection
    except Exception as E:
        print(type(E).__name__, __file__, E.__traceback__.tb_lineno, "\n", E)


if __name__ == "__main__":
    """[summary]"""
    main()
