import webiopi
import time

# import Serial driver
from webiopi.devices.serial import Serial

# initialize Serial driver
serial = Serial("ttyAMA0", 9600)

webiopi.setDebug()

class Show:
    program = ''
    length = 0 # seconds

schedule = []
currentShow = -1 
showStartTime = 0

def setup():
    # empty input buffer before starting processing
    while (serial.available() > 0):
        serial.readString()

def loop():
    global schedule
    global currentShow
    global showStartTime

    #webiopi.debug("loop... schedule count: " + str(len(schedule)))
    if len(schedule) > 0:
        #webiopi.debug("running schedule")
        currentTime = int(time.time())
        if (currentShow == -1) or ((currentTime - showStartTime) > schedule[currentShow].length):
            currentShow += 1

            if currentShow >= len(schedule):
                currentShow = 0

            showStartTime = currentTime
            webiopi.debug("next show: " + schedule[currentShow].program + " for " + str(schedule[currentShow].length) + " seconds");
            serial.writeString(schedule[currentShow].program)
            serial.writeString("\r")

    webiopi.sleep(1)

@webiopi.macro
def setProgram(program):
    global schedule
    schedule = []

    serial.writeString(program)
    serial.writeString("\r")

    return 1

@webiopi.macro
def setSchedule(newSchedule):
    global schedule
    global currentShow
    global showStartTime

    programs = newSchedule.split(";")

    for p in programs:
        parts = p.split(":");
        newShow = Show()
        newShow.program = parts[0]
        newShow.length = int(parts[1])
        webiopi.debug("adding show '" + newShow.program + "' for " + str(newShow.length) + " seconds");
        schedule.append(newShow)

    currentShow = -1
    showStartTime = int(time.time())

    return 1 
