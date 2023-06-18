#!/usr/bin/env python3

import sys
import time
import argparse
import usb.core

activateMic = [1]
deactivateMic = [0]

def main():
    parser = argparse.ArgumentParser(
                        prog="C920e.py",
                        description="Enable/disable the microphone of Logitech C920e webcams")
    parser.add_argument("microphone_state", choices=['on', 'off'])
    args = parser.parse_args()

    devCount = 0
    cameras = usb.core.find(find_all=True, idVendor=0x046d, idProduct=0x08b6)
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
            camera.ctrl_transfer(0x21, 0x01, 0x1000, 0x0b00, activateMic if args.microphone_state == "on" else deactivateMic)
        except usb.core.USBError as e:
            # This exception (usb.core.USBError: [Errno 5] Input/Output Error) is expected because the device disconnects once the URB is sent
            if e.errno != 5:
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
