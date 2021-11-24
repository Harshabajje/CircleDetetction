import revpimodio2
import time
from os import statvfs

class PosValSlave():
    def __init__(self):

        # Change value based on device number visible in webLogin PiCtory
        self.rpi = revpimodio2.RevPiModIODriver(64, autorefresh=True)

        # Manage signals from the operating system for "End program"
        # or Ctrl + C Signal - The driver will then exit properly
        self.rpi.handlesignalend()

        # Use input bytes 0  as int for position X
        self.rpi.io.Input_0.replace_io("PosX", "L")

        # Use input byte 1 as int for Position Y
        self.rpi.io.Input_1.replace_io("PosY", "B")

        # Input byte 2 as int for Position Z
        self.rpi.io.Input_2.replace_io("PosZ", "H")

def cyclefunction(self, cycletools):
        "" "This function is called cyclically by RevPiModIODriver." ""
        # Setting position X, Y, Z values
        self.rpi.io.PosX.value = 100

        self.rpi.io.PosY.value = 200

        self.rpi.io.PosZ.value = 300

def start(self):
        "" "Starts the cycle loop, which calls the cycle function cyclically." ""
        # The program blocks here and works the data cyclically.
        # We set the cycle time to 1000 milliseconds, that's enough for us
        self.rpi.cycleloop(self.cyclefunction, cycletime=1000)

if __name__ == "__main__":
    root = PosValSlave()
    root.start()