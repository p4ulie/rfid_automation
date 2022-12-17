# Loop example:

        if conveyor_sensor == 0:
            print("RFID tag detected")
            print("Enable RFID reader")
            time.sleep(0.2) # wait for RFID reader to initialize
            print("Read output of RFID reader")
            print("Disable RFID reader")
            print("Store time, RFID tag id to DB")
            print("Send signal with RFID reading result to result GPIO port (OK/NOK = 1/0)")
            print("Send signal to indicate the cycle ended to another GPIO port")