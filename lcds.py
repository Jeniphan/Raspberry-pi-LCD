#!/usr/bin/env python


# Written By Cyrus Wolf
# Can be modified and is under the Open Source Standard Rules
# Please pay attention to indents and spacing as it matters with python


# import RPi.GPIO as GPIO #Imports RPi for GPIO Use (Comment/Uncomment to use)
import drivers
import socket  # Imports socket function
import struct  # Imports structure function
import fcntl  # Imports networking function
import time  # Imports time function
import os  # Imports Operating System function
import re  # Imports Reg Ex function
from subprocess import check_output
from time import sleep  # Imports sleep function from time module
import psutil

disp = drivers.Lcd()
# IP = check_output(["hostname", "-I"]).split()[0]

# Sends the Temp of the cpu to the lcd display (for 10 seconds)


def tempcpu():  # Defines "tempcpu"
    for _ in range(10):  # Sets up timer

        # Gets temp reading (shows as "temp=xx.x'C")
        cputemp = os.popen("vcgencmd measure_temp").readline()
        # Removes everything but numbers and "."
        celsius = re.sub("[^0123456789\.]", "", cputemp)
        # Math Function Fahrenheit (celsius * 9 / 5 + 32) as interger
        fahrenheit = int(9.0/5.0*int(float(celsius)+32))

        c_percent = psutil.cpu_percent()
        cpu_freq = psutil.cpu_freq()
        r_m = psutil.virtual_memory()
        
        cpu_freq = cpu_freq.current / 1000
        # Prints Temp as Celsius to the LCD Display line 1
        disp.lcd_display_string("CLK:" + str(cpu_freq) + " CPU:" + str(c_percent) ,1)
        # Prints Temp as Fahrenheit to the LCD Display line 2
        disp.lcd_display_string("RAM:" + str(r_m.percent) + " T:" + str(celsius), 2)

        sleep(1)  # Sleeps for one second before restarting loop

# Sends the Time and Date to the lcd display (for 10 seconds)


def curtime():  # Defines "curtime"
    for _ in range(10):  # Sets up timer

        # Prints time to the LCD Display line 1
        disp.lcd_display_string("Time:  {}".format(time.strftime("%H:%M:%S")), 1)
        # Prints date to the LCD Display line 2
        disp.lcd_display_string("Date: {}".format(time.strftime("%m:%d:%Y")), 2)

        sleep(1)  # Sleeps for one second before restarting loop

# Gets the IP Address


def getaddr():  # Defines "getaddr" as well as ifname arguement later

    cmd = "hostname -I | cut -d\' \' -f1"
    return check_output(cmd, shell=True).decode("utf-8").strip()

def getip():  # Defines "getip"

    # Grabs the address from "wlan0" and assigns it to "ip"
    for _ in range(10):  # Sets up timer

        disp.lcd_display_string("   IP Address:", 1)  # Prints string to LCD Display line 1
        disp.lcd_display_string("  " + getaddr(), 2)  # Prints "ip" to LCD Display line 2

        sleep(1)  # Sleeps for one second before restarting loop


# runs a forever loop calling the defs above
try:  # Gives way to exception later

    while True:  # Forever loop

        tempcpu()  # Calls "tempcpu"
        disp.lcd_clear()  # Clears the LCD Display

        curtime()  # Calls "curtime"
        disp.lcd_clear()  # Clears the LCD Display

        getip()  # Calls "getip"
        disp.lcd_clear()  # Again Clears the LCD Display

# Allows for clean exit
except KeyboardInterrupt:  # If interrupted by the keyboard ("Control" + "C")

    disp.lcd_clear()  # clear the lcd display
    sleep(1)  # sleeps 1 second
# Turn Off Backlight

# Exits the python interperter
exit()

