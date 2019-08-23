
from pyudmx import pyudmx
from time import sleep


def send_rgb(dev, red, green, blue):
    cv = [0 for v in range(0, 512)]
    cv[0] = red
    cv[1] = green
    cv[2] = blue
    sent = dev.send_multi_value(1, cv)
    return sent


def main():
    cv = [0 for v in range(0, 512)]
    dev = pyudmx.uDMXDevice()
    dev.open()
    while True:
        send_rgb(dev, 255, 20, 147)
        sleep(3.0)
        send_rgb(dev, 0, 0, 255)
        sleep(3.0)
    dev.close()


if __name__ == "__main__":
    main()
