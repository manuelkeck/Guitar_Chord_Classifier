import usb.core
from usb.util import get_string


class USBDevice:

    def __init__(self, device):
        self.device = device

    def display_info(device):

        # print(f"Bus {self.device.idProduct:04x}")

        try:
            print(f"{get_string(device, device.iProduct)} from "
                  f"{get_string(device, device.iManufacturer)} found.\nSerial number: "
                  f"{get_string(device, device.iSerialNumber)}")
        except usb.core.USBError:
            print("Device not reachable.")
