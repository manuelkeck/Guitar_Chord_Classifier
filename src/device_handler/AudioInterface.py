import usb.core
import sounddevice as sd

from usb.util import get_string


class AudioInterface:
    """
    This class will find the usb audio interface by idVendor and idProduct which has to be determined before usage.
    This is needed to get the device index to record audio streams.
    """
    @staticmethod
    def find_device():
        """
        This function will find the audio interface by given idVendor and idProduct if its connected.
        :return: Object of device with corresponding index (USB)
        """
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
        """
        This function displays some information about the audio interface.
        :param device: Found device by idVendor and idProduct from find_device() function
        :param index: Index from usb device, identified in find_device() function
        :return: None
        """
        try:
            print(f"Product: {get_string(device, device.iProduct)}\n"
                  f"Manufacturer: {get_string(device, device.iManufacturer)}\n")
            print(f"Searching index from {get_string(device, device.iProduct)}...")
            print(f"Index found at position {index}.")
        except usb.core.USBError:
            print("Device not reachable.")

    @staticmethod
    def get_device_index(device):
        """
        This function will find the index from usb audio interface by its name. The function is called from
        find_device().
        :param device: Found device by idVendor and idProduct from find_device() function
        :return: Index of device if found
        """
        keyword = get_string(device, device.iProduct)
        device_list = sd.query_devices()

        for i, device in enumerate(device_list):
            device_name = device.get('name', '')
            if keyword in device_name:
                return i

        return None
