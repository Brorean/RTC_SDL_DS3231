#!/usr/bin/env python3

# *-----------------------------------------------------------------------------*
# * DS3231/DS3232 Alarm Example #4                                              *
# *                                                                             *
# * Set Alarm 1 to occur every second.                                          *
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


def main():
    global _rtc

    signal.signal(signal.SIGINT, sig_handler)

    _rtc = SDL_DS3231.SDL_DS3231(1, 0x68)
    clearRTCAlarms(_rtc)

    # set the RTC to an arbitrary time
    _rtc.write_all(seconds=0, minutes=0, hours=0, date=16, month=9, year=(2017-1970), save_as_24h=True)

    # set Alarm 1 to occur once per second
    _rtc.setAlarm(_rtc.ALM1_EVERY_SECOND, 0, 0, 0, 0)
    # clear the alarm flag
    _rtc.alarm(_rtc.ALARM_1)

    print("%s Start %s" % (time.time(), _rtc.read_str()))

    while True:
        # check to see if the alarm flag is set (also resets the flag if set)
        if ( _rtc.alarm(_rtc.ALARM_1) ):
            print("%s ALARM_1 %s" % (time.time(), _rtc.read_str()))


if __name__ == "__main__":
    main()
