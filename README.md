# Loop example:

        if conveyor_sensor GPIO port 0 == 1:
            "Set 0 to GPIO port 5"
            "Set 0 to GPIO port 6"

            result = "Read output of RFID reader (timeout?)"

            print("Store time, RFID tag (even not sucessfull read with null) id to DB")

            if result:
                OK  = print("Set 1 to GPIO port 5")
                NOK = print("Set 1 to GPIO port 6")

