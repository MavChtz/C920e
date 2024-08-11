#!/usr/bin/env python3

import sys
import time
import argparse
import usb.core

ACTIVATE_MIC = [1]
DEACTIVATE_MIC = [0]
SUPPORTED_CAMERA_IDS = {
    0x08b6: "Logi Webcam C920e",
    0x08b7: "Logi Webcam C920e",
    0x085b: "Logi Webcam C925e",
}

VENDOR_LOGITECH = 0x046d
VENDOR_LOGITECH_STR = "Logitech, Inc."

def format_supported_cameras():
    res = ""
    for id, name in SUPPORTED_CAMERA_IDS.items():
        res += f"{VENDOR_LOGITECH:0{4}x}:{id:0{4}x} {VENDOR_LOGITECH_STR} {name}\n"
    return res

def main():
    parser = argparse.ArgumentParser(
                        prog="C920e.py",
                        formatter_class=argparse.RawDescriptionHelpFormatter,
                        description="Enable/disable the microphone of Logitech C9XXe series webcams.\n\nsupported devices:\n" + format_supported_cameras())
    parser.add_argument("microphone_state", choices=['on', 'off'])
    args = parser.parse_args()

    devCount = 0
    cameras = usb.core.find(find_all=True, custom_match=lambda d: d.idVendor == VENDOR_LOGITECH and d.idProduct in SUPPORTED_CAMERA_IDS)
    for camera in cameras:
        devCount += 1
        print(f"Configuring microphone on device: {devCount}")

        cfg = camera[0]
        for intf in range(cfg.bNumInterfaces):
            try:
                if camera.is_kernel_driver_active(intf):
                    camera.detach_kernel_driver(intf)
            except usb.core.USBError as e:
                if e.errno == 13:
                    print("ERROR: Permission denied, run this script with sudo or as root.")
                else:
                    print(f"Unexpected error: {e}")
                sys.exit(1)

        camera.set_configuration()
        try:
            camera.ctrl_transfer(0x21, 0x01, 0x1000, 0x0b00, ACTIVATE_MIC if args.microphone_state == "on" else DEACTIVATE_MIC)
        except usb.core.USBError as e:
            # These exceptions are expected because the device disconnects once the URB is sent:
            # - usb.core.USBError: [Errno 5] Input/Output Error
            # - usb.core.USBError: [Errno 19] No such device (it may have been disconnected)
            if e.errno != 5 and e.errno != 19:
                print(f"Unexpected error:\n{e}")
                continue

        time.sleep(1)
        print(f"Microphone configuration successful on device: {devCount}", end="\n\n")

    if devCount == 0:
        print("ERROR: No compatible devices found.\nIf you've run this script already, make sure to replug your devices.")
        sys.exit(2)

    print(f"SUCCESS: Please unplug and replug your camera{'s' if devCount > 1 else ''}.")

if  __name__ == "__main__":
    main()
