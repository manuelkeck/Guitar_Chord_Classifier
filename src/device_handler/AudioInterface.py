import usb.core
import sounddevice as sd

from usb.util import get_string


class AudioInterface:
    @staticmethod
    def find_device():

        # idVendor and idProduct determined via linux terminal 'lsusb'
        device = usb.core.find(idVendor=0x0499, idProduct=0x172f)

        if device is not None:
            index = AudioInterface.get_device_index(device)
            AudioInterface.display_info(device, index)
            return device, index
        else:
            print("Steinberg device not found.")

        return None, None

    @staticmethod
    def display_info(device, index):

        try:
            print(f"Product: {get_string(device, device.iProduct)}\n"
                  f"Manufacturer: {get_string(device, device.iManufacturer)}\n")
            print(f"Searching index from {get_string(device, device.iProduct)}...")
            print(f"Index found at position {index}.")
        except usb.core.USBError:
            print("Device not reachable.")

    @staticmethod
    def get_device_index(device):

        keyword = get_string(device, device.iProduct)
        device_list = sd.query_devices()

        for i, device in enumerate(device_list):
            device_name = device.get('name', '')
            if keyword in device_name:
                return i

        return None
