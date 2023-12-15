import usb.core
from source.USBDevice import USBDevice


class ListUSBDevices:

    @staticmethod
    def list_usb_devices():

        devices = usb.core.find(find_all=True)

        if devices is None:
            print("No connected USB device found.")
            return

        for device in devices:
            usb_device = USBDevice(device)
            usb_device.display_info()
