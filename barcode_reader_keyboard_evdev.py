from evdev import InputDevice, categorize, ecodes

INPUT_DEVICE = "/dev/input/by-id/usb-BARCODE_SCANNER_Keyboard_Interface_FFFFFFFFFFFF-event-kbd"
device = InputDevice(INPUT_DEVICE)
for event in device.read_loop():
    print(event)
    if event.type == ecodes.EV_KEY:
        print(categorize(event))

