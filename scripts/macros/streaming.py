import webiopi

# import Serial driver
from webiopi.devices.serial import Serial

# initialize Serial driver
serial = Serial("ttyAMA0", 9600)

def setup():
    # empty input buffer before starting processing
    while (serial.available() > 0):
        serial.readString()

data = ''
def loop():
    global data 
    if (serial.available() > 0):
        data = serial.readString()     # read available data

    webiopi.sleep(1)


@webiopi.macro
def sendData(data):
    serial.writeString(data);
    if (data != '+++'):
        serial.writeString("\r");

@webiopi.macro
def getData():
    global data

    tmp = data;
    data = '';
    return tmp;
