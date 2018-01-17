#!/usr/bin/env python3

# *-----------------------------------------------------------------------------*
# * DS3231/DS3232 Alarm Example #1                                              *
# *                                                                             *
# * Set Alarm 1 to occur once a minute at 5 seconds after the minute.           *
# * Detect the alarm by polling the RTC alarm flag.                             *
# *                                                                             *
# * Hardware:                                                                   *
# * Raspberry Pi, DS3231 RTC.                                                   *
# * Connect RTC SDA to Raspberry Pi pin 3 (GPIO2).                              *
# * Connect RTC SCL to Raspberry Pi pin 5 (GPIO3).                              *
# *                                                                             *
# * The original test case from Jack Christensen 16Sep2017                      *
# * Rewritten for python3 on 16Jan18                                            *
# *-----------------------------------------------------------------------------*

import datetime
import signal
import sys
import time

import SDL_DS3231

_rtc = None

# Handle ctrl-c from user and clean up
def sig_handler(signum, frame):
    global _rtc
    clearRTCAlarms(_rtc)
    print("Quitting...")
    quit()

# initialize the alarms to known values, clear the alarm flags, clear the alarm interrupt flags
def clearRTCAlarms(rtc):
    rtc.setAlarm(rtc.ALM1_MATCH_DATE, 0, 0, 0, 1)
    rtc.setAlarm(rtc.ALM2_MATCH_DATE, 0, 0, 0, 1)
    rtc.alarm(rtc.ALARM_1)
    rtc.alarm(rtc.ALARM_2)
    rtc.alarmInterrupt(rtc.ALARM_1, False)
    rtc.alarmInterrupt(rtc.ALARM_2, False)
    rtc.squareWave(rtc.SQWAVE_NONE)

# set the RTC time and date from the raspberry pi
def raspberryPiTimeSet(rtc):
    now = datetime.datetime.now()

    rtc.write_datetime(now)


def main():
    global _rtc

    signal.signal(signal.SIGINT, sig_handler)

    _rtc = SDL_DS3231.SDL_DS3231(1, 0x68)
    clearRTCAlarms(_rtc)

    raspberryPiTimeSet(_rtc)

    # set Alarm 1 to occur at 5 seconds after every minute
    _rtc.setAlarm(_rtc.ALM1_MATCH_SECONDS, 5, 0, 0, 1)
    # clear the alarm flag
    _rtc.alarm(_rtc.ALARM_1)

    print("%s Start %s" % (time.time(), _rtc.read_str()))

    while True:
        if ( _rtc.alarm(_rtc.ALARM_1) ): # check alarm flag, clear it if set
            print("%s ALARM_1 %s" % (time.time(), _rtc.read_str()))

        if ( _rtc.alarm(_rtc.ALARM_2) ): # check alarm flag, clear it if set
            print("%s ALARM_2 %s" % (time.time(), _rtc.read_str()))

        time.sleep(1)

if __name__ == "__main__":
    main()
