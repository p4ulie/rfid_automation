import asyncio
import configparser
import time
from evdev import InputDevice, categorize, ecodes
from evdev_text_wrapper_asyncio import scancodes, capscodes, evdev_readline

# async def helper(dev):
#     async for ev in dev.async_read_loop():
#         print(repr(ev))

async def main():
    print("Before wait")
    result = None
    try:
        result = await asyncio.wait_for(evdev_readline(rfid_reader), 3)
    except asyncio.TimeoutError:
        result = 'timeout'
    finally:
        print("After wait, result:", result)

    return result

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('settings.ini')

    rfid_reader = InputDevice(config['RfidReaderDeviceSettings']['Name'])
    rfid_reader_timeout = config['RfidReaderDeviceSettings']['Timeout']
    rfid_reader.grab()

    result = asyncio.run(main())

    print("Result: %s" % result)

    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(helper(rfid_reader))

    print("========================================")
