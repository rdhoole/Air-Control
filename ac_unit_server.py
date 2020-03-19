#!/usr/bin/env python

#TODO: FIX GET_AVERAGE_TEMP TO PROPERLY CREATE STRING FOR COMMAND

import socket, time, signal
from subprocess import check_output
from threading import Thread

MAXDATA = 2048
COMPUTERS = ["pi@0.0.0.0"]

Compressor      = False
fan             = False
fan_toggle      = False
auto_ac         = False

ac_on  = 85
ac_off = 80

def sigterm_handler(_signo, _stack_frame):
    sys.exit(0)

def serverMain():

    #make sure we have everything off
    global COMPUTERS, compressor, fan
    print("Cleaning up...")

    compressor = True
    fan = True
    for computer in COMPUTERS:
        setACTUATOR_OFF(computer)
        setAC_OFF(computer)
    print("Starting Watchdog...")
    auto_thread.start()
    print("Starting Server...")
    host = "0.0.0.0"
    port = 1212

    ss = socket.socket()
    ss.bind((host, port))
    ss.listen(2)
    print("OK.")
    while True:
        connection, address = ss.accept()
        serverWork(connection)

def serverWork(connection):
    global MAXDATA
    try:
        command = connection.recv(MAXDATA).decode()
        if not command:
	        print("Error: command not understood")
        else:
	        connection.send(serverCommands(command.rstrip()).encode())
    except Exception as e:
        print("Error: " + str(e))

    connection.close()
def serverCommands(command):
    global COMPUTERS
    answer = ""
    command = command.split(" ")

    if (command[0] == "GET_TEMP"):
        if (len(command) > 1):
	        for computer in (command[1:]):
		        answer += getTemp(computer)
	        return str(answer)
        else:
	        for computer in COMPUTERS:
		        answer += getTemp(computer)
	        return str(answer)
    if (command[0] == "GET_AVERAGE_TEMP"):
        average = 0
        if (len(command) > 1):
        # TODO:
        # THE TOP PART OF CODE DOES NOT WORK!!!
        # THIS IS HERE JUST INCASE WE WANT TO
        # ADD THE FEATURE OF GETTING AVERAGES
        # FROM CERTAIN DEVICES NAMED...
	        temps = serverCommands("GET_TEMP" + command[1:]).split(":")[1::2]
	        count = len(temps)
	        for temp in temps:
		        average += int(temp.split("F")[0].split(" ")[1])
	        return str(int(average/count)) + "F"
        else:
	        temps = serverCommands("GET_TEMP").split(":")[1::2]
	        count = len(temps)
	        for temp in temps:
		        average += int(temp.split("F")[0].split(" ")[1])
	        return str(int(average/count)) + "F"
    if (command[0] == "GET_SETTINGS"):
        for computer in COMPUTERS:
	        answer += getSettings()
        return str(answer)
    if (command[0] == "SET_SETTINGS"):
        # take only 2 settings... ac_on ac_off
        if (len(command) > 2 and len(command) < 5):
	        answer += setSettings(command[1], command[2], command[3])
	        return str(answer)
        else:
	        answer += "Failed: need settings"
	        return str(answer)
    if (command[0] == "AC_ON"):
        if (len(command) > 1):
	        for computer in (command[1:]):
		        answer += setAC_ON(computer)
	        return str(answer)
        else:
	        for computer in COMPUTERS:
		        answer += setAC_ON(computer)
	        return str(answer)
    if (command[0] == "AC_OFF"):
        if (len(command) > 1):
	        for computer in (command[1:]):
		        answer += setAC_OFF(computer)
	        return str(answer)
        else:
	        for computer in COMPUTERS:
		        answer += setAC_OFF(computer)
	        return str(answer)
    if (command[0] == "TOGGLE_AC"):
        if (len(command) > 1):
	        for computer in (command[1:]):
		        answer += toggleAC(computer)
	        return str(answer)
        else:
	        for computer in COMPUTERS:
		        answer += toggleAC(computer)
	        return str(answer)
    if (command[0] == "FAN"):
        if (len(command) > 1):
	        for computer in (command[1:]):
		        answer += setFAN_ON(computer)
	        return str(answer)
        else:
	        for computer in COMPUTERS:
		        answer += setFAN_ON(computer)
	        return str(answer)
    if (command[0] == "FAN_OFF"):
        if (len(command) > 1):
	        for computer in (command[1:]):
		        answer += setFAN_OFF(computer)
	        return str(answer)
        else:
	        for computer in COMPUTERS:
		        answer += setFAN_OFF(computer)
	        return str(answer)
    if (command[0] == "TOGGLE_FAN"):
        if (len(command) > 1):
	        for computer in (command[1:]):
		        answer += toggleFAN(computer)
	        return str(answer)
        else:
	        for computer in COMPUTERS:
		        answer += toggleFAN(computer)
	        return str(answer)
    if (command[0] == "ACTUATOR_ON"):
        if (len(command) > 1):
	        for computer in (command[1:]):
		        answer += setACTUATOR_ON(computer)
	        return str(answer)
        else:
	        for computer in COMPUTERS:
		        answer += setACTUATOR_ON(computer)
	        return str(answer)
    if (command[0] == "ACTUATOR_OFF"):
        if (len(command) > 1):
	        for computer in (command[1:]):
		        answer += setACTUATOR_OFF(computer)
	        return str(answer)
        else:
	        for computer in COMPUTERS:
		        answer += setACTUATOR_OFF(computer)
	        return str(answer)
    else:
        return "Unrecognized command."

#### talk to computers
def runCommand(command):
    return check_output(command).decode("utf-8")

def setSettings(ac_on_, ac_off_, auto_ac_):
    global ac_on, ac_off, auto_ac, auto_thread
    ac_on = int(ac_on_)
    ac_off = int(ac_off_)
    auto_ac = True if str(auto_ac_) == "True" else False

    auto_thread.join(0.1)
    auto_thread = Thread(target=autoMode)
    auto_thread.start()

    return "Set"

def getSettings():
    global ac_on, ac_off, auto_ac
    return str(ac_on) + ":" + str(ac_off) + ":" + str(auto_ac)

def getTemp(address):
    command = ["ssh", address, "sudo", "python", "get_temp.py"]
    return address + ": " + runCommand(command) + ": "

def setAC_ON(address):
    global compressor, fan
    if not compressor and not fan:
        setFAN_ON(address)
        setCOMPRESSOR(address)
    if not compressor and fan:
        setCOMPRESSOR(address)
    return address + ": AC On"
def setAC_OFF(address):
    global fan_toggle
    if not fan_toggle:
        setCOMPRESSOR_OFF(address)
        setFAN_OFF(address)
    else:
        setCOMPRESSOR_OFF(address)
    return address + ": AC Off"

def toggleAC(address):
    global compressor, auto_ac
    if auto_ac:
        auto_ac = False
    if compressor:
        return setAC_OFF(address)
    else:
        return setAC_ON(address)

def setCOMPRESSOR(address):
    global compressor
    if not compressor:
        command = ["ssh", address, "sudo", "python", "compressor-control.py", "-o", "on"]
        runCommand(command)
        compressor = True
    return address + ": Compressor on"

def setCOMPRESSOR_OFF(address):
    global compressor
    if compressor:
        command = ["ssh", address, "sudo", "python", "compressor-control.py", "-o", "off"]
        runCommand(command)
        compressor = False
    return address + ": Compressor off"

def setFAN_ON(address):
    global fan
    if not fan:
        command = ["ssh", address, "sudo", "python", "fan-control.py", "-o", "on"]
        runCommand(command)
        fan = True
    return address + ": Fan on"

def setFAN_OFF(address):
    global compressor,fan
    if not compressor and fan:
        command = ["ssh", address, "sudo", "python", "fan-control.py", "-o", "off"]
        runCommand(command)
        fan = False
        return address + ": Fan off"
    if compressor:
        return address + ": Compressor On, fan failed to shut off."

def toggleFAN(address):
    global fan, fan_toggle, compressor
    if fan and compressor:
        fan_toggle = not fan_toggle
        return address + ": Toggle fan with AC on."
    elif fan and not compressor:
        fan_toggle = False
        return setFAN_OFF(address)
    else:
        fan_toggle = True
        return setFAN_ON(address)

def setACTUATOR_ON(address):
    command = ["ssh", address, "sudo", "python", "actuator-control.py", "-o", "on"]
    return address + ": " + runCommand(command)

def setACTUATOR_OFF(address):
    command = ["ssh", address, "sudo", "python", "actuator-control.py", "-o", "off"]
    return address + ": " + runCommand(command)

def autoMode():
    global auto_ac,ac_on,ac_off
    averageTemp = 0
    while auto_ac:
        averageTemp = int(serverCommands("GET_AVERAGE_TEMP").split("F")[0])
        if (averageTemp >= ac_on):
	        serverCommands("AC_ON")
        elif (averageTemp <= ac_off):
	        serverCommands("AC_OFF")
        time.sleep(5)
    print("Watchdog: done.")

auto_thread = Thread(target=autoMode)
if __name__ == '__main__':
    signal.signal(signal.SIGTERM, sigterm_handler)
    try:
        serverMain()
    finally:
        auto_ac = False
        auto_thread.join()
