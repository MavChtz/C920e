# Description
This script enables or disables the microphone on the Logitech C920e webcam for Linux, eliminating the need to use Logi Tune on a Windows computer.

# Requirements
This program requires the following packages:
```
Python >= 3.7,
pyusb >= 1.0
```
Depending on your system, pick one of the following commands and run it in a terminal:

### Debian/Ubuntu:
```
sudo apt install git python3-usb
```

### Arch based:
```
sudo pacman -S git python-pyusb
```

### Fedora:
```
sudo dnf install git python3-pyusb
```

### OpenSUSE:
```
sudo zypper install git python-pyusb
```

### pip:

```
python -m pip install pyusb
```

# Usage

## Download
```
git clone https://github.com/MavChtz/C920e
cd C920e
```
Then:

## To enable the microphone on all supported cameras:
```
sudo ./C920e.py on
```

## To disable the microphone on all supported cameras: 
```
sudo ./C920e.py off
```