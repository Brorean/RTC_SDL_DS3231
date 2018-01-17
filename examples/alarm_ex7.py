#!/usr/bin/env python3

# *-----------------------------------------------------------------------------*
# * DS3231/DS3232 Alarm Example #7                                              *
# *                                                                             *
# * Set Alarm 2 to occur at a given time hh:mm.                                 *
# * Configure the RTC INT/SQW pin to be asserted when alarm match occurs.       *
# * Detect the alarm by polling the INT/SQW pin.                                *
# *                                                                             *
# * Hardware:                                                                   *
# * Raspberry Pi, DS3231 RTC.                                                   *
# * Connect RTC SDA to Raspberry Pi pin 3 (GPIO2).                              *
# * Connect RTC SCL to Raspberry Pi pin 5 (GPIO3).                              *
# * Connect RTC INT/SQW to Raspberry Pi pin 7 (GPIO4).                          *
# *                                                                             *
# * The original test case from Jack Christensen 16Sep2017                      *
# * Rewritten for python3 on 16Jan18                                            *
# *-----------------------------------------------------------------------------*

import datetime
import RPi.GPIO as GPIO
import signal
import sys
import time

import SDL_DS3231

ALARM_PIN = 7
_rtc = None
_tLast = None

# Handle ctrl-c from user and clean up
def sig_handler(signum, frame):
    global _rtc
    GPIO.remove_event_detect(ALARM_PIN)
    GPIO.cleanup()
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
    global _tLast

    signal.signal(signal.SIGINT, sig_handler)

    _rtc = SDL_DS3231.SDL_DS3231(1, 0x68)
    clearRTCAlarms(_rtc)

    # Setup the GPIO pins
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(ALARM_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # Add event handler to trigger when INT/SQW pin goes low
    GPIO.add_event_detect(ALARM_PIN, GPIO.FALLING)

    # set the RTC time to 06:29:50
    _rtc.write_all(seconds=50, minutes=29, hours=6, date=16, month=9, year=(2017-1970), save_as_24h=True)

    # set Alarm 2 for 06:30:00
    _rtc.setAlarm(_rtc.ALM2_MATCH_HOURS, 0, 30, 6, 0)
    # clear the alarm flags
    _rtc.alarm(_rtc.ALARM_1)
    _rtc.alarm(_rtc.ALARM_2)

    # configure the INT/SQW pin for "interrupt" operation (disable square wave output)
    _rtc.squareWave(_rtc.SQWAVE_NONE)

    # enable interrupt output for Alarm 2 only
    _rtc.alarmInterrupt(_rtc.ALARM_1, False)
    _rtc.alarmInterrupt(_rtc.ALARM_2, True)

    print("%s Start %s" % (time.time(), _rtc.read_str()))

    while True:
        # check to see if the INT/SQW pin is low, i.e. an alarm has occurred
        if GPIO.event_detected(ALARM_PIN):
            # check to see if the alarm flag is set (also resets the flag if set)
            if ( _rtc.alarm(_rtc.ALARM_2) ):
                print("%s ALARM_2 %s" % (time.time(), _rtc.read_str()))

        # print the time when it changes
        now = _rtc.read_datetime()
        if _tLast is None:
            _tLast = now
        if ( now != _tLast ):
            _tLast = now
            print(_rtc.read_str())



if __name__ == "__main__":
    main()
