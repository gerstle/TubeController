import webiopi
import time
import urllib

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

fadeOutShow = Show()
fadeOutShow.program = 'fadeout'
fadeOutShow.length = 2

def setup():
    # empty input buffer before starting processing
    while (serial.available() > 0):
        serial.readString()

    # setup an initial schedule
    newShow = Show()
    newShow.program = "melt"
    newShow.length = 1200
    schedule.append(newShow)
    schedule.append(fadeOutShow)

    newShow = Show()
    newShow.program = "melt sparkle"
    newShow.length = 1200
    schedule.append(newShow)
    schedule.append(fadeOutShow)

    currentShow = -1
    showStartTime = int(time.time())

    # send fade out to end the current thing smoothly
    serial.writeString('push fadeout')
    serial.writeString("\r")

def loop():
    global schedule
    global currentShow
    global showStartTime

    #webiopi.debug("loop... schedule count: " + str(len(schedule)))
    if len(schedule) > 0:
        #webiopi.debug("running schedule")
        currentTime = int(time.time())
        if (currentShow == -1) or ((currentTime - showStartTime) > schedule[currentShow].length):
            # currentShow == -1 means we're starting a schedule for the first time... give time to fade out of previous
            if (currentShow == -1):
                time.sleep(2)
            
            currentShow += 1

            if (currentShow >= len(schedule)):
                currentShow = 0

            showStartTime = currentTime
            webiopi.debug("next show: " + schedule[currentShow].program + " for " + str(schedule[currentShow].length) + " seconds");

            if (schedule[currentShow].program != 'fadeout'):
                serial.writeString("program ")
            else:
                serial.writeString("push ")

            serial.writeString(schedule[currentShow].program)
            if (schedule[currentShow].program != 'fadeout'):
                serial.writeString(" fadein")
            serial.writeString("\r")

    webiopi.sleep(1)

@webiopi.macro
def setProgram(program):
    global schedule
    schedule = []

    # send fade out to end the current thing smoothly
    serial.writeString('push fadeout')
    serial.writeString("\r")

    time.sleep(2);

    serial.writeString("program ")
    serial.writeString(urllib.parse.unquote(program))
    serial.writeString(" fadein")
    serial.writeString("\r")

    return 1

@webiopi.macro
def setSchedule(newSchedule):
    global schedule
    global currentShow
    global showStartTime
    global fadeOutShow

    del schedule[:]
    programs = newSchedule.split(";")

    for p in programs:
        parts = p.split(":");
        newShow = Show()
        newShow.program = urllib.parse.unquote(parts[0])
        newShow.length = int(parts[1])
        webiopi.debug("adding show '" + newShow.program + "' for " + str(newShow.length) + " seconds");
        schedule.append(newShow)

        # append a fadeOut for every program... fadeIn is added by the loop above 
        schedule.append(fadeOutShow)

    currentShow = -1
    showStartTime = int(time.time())

    # send fade out to end the current thing smoothly
    serial.writeString('push fadeout')
    serial.writeString("\r")

    return 1 
