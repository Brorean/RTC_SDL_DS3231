#!/usr/bin/env python3

# *----------------------------------------------------------------------*
# * DS3232RTC library, example sketch to demonstrate usage of            *
# * the alarm interrupt for alarm 1 and alarm 2.                         *
# *                                                                      *
# * Notes:                                                               *
# * Using the INT/SQW pin for alarms is mutually exclusive with using    *
# * it to output a square wave. However, alarms can still be set when    *
# * a square wave is output, but then the alarm() function will need     *
# * to be used to determine if an alarm has triggered. Even though       *
# * the DS3231 power-on default for the INT/SQW pin is as an alarm       *
# * output, it's good practice to call RTC.squareWave(SQWAVE_NONE)       *
# * before setting alarms.                                               *
# *                                                                      *
# * I recommend calling RTC.alarm() before RTC.alarmInterrupt()          *
# * to ensure the RTC's alarm flag is cleared.                           *
# *                                                                      *
# * The RTC's time is updated on the falling edge of the 1Hz square      *
# * wave (whether it is output or not). However, the Arduino Time        *
# * library has no knowledge of this, as its time is set asynchronously  *
# * with the RTC via I2C. So on average, it will be 500ms slow           *
# * immediately after setting its time from the RTC. This is seen        *
# * in the sketch output as a one-second difference because the          *
# * time returned by now() has not yet rolled to the next second.        *
# *                                                                      *
# * Hardware:                                                            *
# * Raspberry Pi, DS3231 RTC.                                            *
# * Connect RTC SDA to Raspberry Pi pin 3 (GPIO2).                       *
# * Connect RTC SCL to Raspberry Pi pin 5 (GPIO3).                       *
# * Connect RTC INT/SQW to Raspberry Pi pin 7 (GPIO4).                   *
# *                                                                      *
# * The original test case from Jack Christensen 16Sep2017               *
# * Rewritten for python3 on 16Jan18                                     *
# *----------------------------------------------------------------------*

import datetime
import RPi.GPIO as GPIO
import signal
import sys
import time

import SDL_DS3231

ALARM_PIN = 7
_rtc = None
_is_interrupt_triggered = False

# Code when interrupt happens this method is called
def interrupt_handler(pin):
    global _is_interrupt_triggered
    _is_interrupt_triggered = True

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

# set the RTC time and date from the raspberry pi
def raspberryPiTimeSet(rtc):
    now = datetime.datetime.now()

    rtc.write_datetime(now)


def main():
    global _is_interrupt_triggered
    global _rtc

    signal.signal(signal.SIGINT, sig_handler)

    _rtc = SDL_DS3231.SDL_DS3231(1, 0x68)
    clearRTCAlarms(_rtc)
    raspberryPiTimeSet(_rtc)

    # Setup the GPIO pins
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(ALARM_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # Add event handler to trigger when INT/SQW pin goes low
    GPIO.add_event_detect(ALARM_PIN, GPIO.FALLING)
    # Add event call back, when pin goes low call interrupt_handler method
    GPIO.add_event_callback(ALARM_PIN, interrupt_handler)

    # set alarm 1 for 20 seconds after every minute
    _rtc.setAlarm(_rtc.ALM1_MATCH_SECONDS, 20, 0, 0, 1) #  daydate parameter should be between 1 and 7
    _rtc.alarm(_rtc.ALARM_1)  # ensure RTC interrupt flag is cleared
    _rtc.alarmInterrupt(_rtc.ALARM_1, True)  # Make the DS3231 int pin active for ALARM_1

    # set alarm 2 for every minute
    _rtc.setAlarm(_rtc.ALM2_EVERY_MINUTE, 0, 0, 0, 1)
    _rtc.alarm(_rtc.ALARM_2)  # ensure RTC interrupt flag is cleared
    _rtc.alarmInterrupt(_rtc.ALARM_2, True) # Make the DS3231 int pin active for ALARM_2

    print("%s Start %s" % (time.time(), _rtc.read_str()))

    while True:
        if (_is_interrupt_triggered):
            if ( _rtc.alarm(_rtc.ALARM_1) ):
                print("%s ALARM_1 %s" % (time.time(), _rtc.read_str()))
            if ( _rtc.alarm(_rtc.ALARM_2) ):
                print("%s ALARM_2 %s" % (time.time(), _rtc.read_str()))

            _is_interrupt_triggered = False


if __name__ == "__main__":
    main()
