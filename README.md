
# Raspberry Pi Python Library for DS3231/AT24C32 RTC Module
This is a fork of the Raspberry Pi Python Library for SwitchLabs DS3231/AT24C32 RTC

Using code based on the Arduino DS3232RTC by Jack Christensen added new methods to the SwitchLabs
library to set and handle alarms from the DS3231 RTC modules.

### The examples director has several examples on how to set and read if an alarm has been triggered

### The new methods are:

### alarmNumber
##### Description
Symbolic names used for Alarm 1 or Alarm 2
##### Values
- ALARM_1 -- for Alarm 1
- ALARM_2 -- for Alarm 2

### freq
##### Description
Symbolic names used with the squareWave() method (described below).
##### Values
- SQWAVE_NONE
- SQWAVE_1_HZ
- SQWAVE_1024_HZ
- SQWAVE_4096_HZ
- SQWAVE_8192_HZ

### alarmType
##### Description
Symbolic names used with the setAlarm() method (described below).
##### Values for Alarm 1
- ALM1_EVERY_SECOND -- causes an alarm once per second.
- ALM1_MATCH_SECONDS -- causes an alarm when the seconds match (i.e. once per minute).
- ALM1_MATCH_MINUTES -- causes an alarm when the minutes *and* seconds match.
- ALM1_MATCH_HOURS -- causes an alarm when the hours *and* minutes *and* seconds match.
- ALM1_MATCH_DATE -- causes an alarm when the date of the month *and* hours *and* minutes *and* seconds match.
- ALM1_MATCH_DAY -- causes an alarm when the day of the week *and* hours *and* minutes *and* seconds match.

##### Values for Alarm 2
- ALM2_EVERY_MINUTE -- causes an alarm once per minute.
- ALM2_MATCH_MINUTES -- causes an alarm when the minutes match (i.e. once per hour).
- ALM2_MATCH_HOURS -- causes an alarm when the hours *and* minutes match.
- ALM2_MATCH_DATE -- causes an alarm when the date of the month *and* hours *and* minutes match.
- ALM2_MATCH_DAY -- causes an alarm when the day of the week *and* hours *and* minutes match.

### setAlarm(self, alarmType, seconds, minutes, hours, daydate)
##### Description
Set an alarm time. Sets the alarm registers only.  To cause the INT pin to be asserted on alarm match, use alarmInterrupt(). This method can set either Alarm 1 or Alarm 2, depending on the value of alarmType (See above). When setting Alarm 2, the seconds value must be supplied but is ignored, recommend using zero. (Alarm 2 has no seconds register.)

##### Syntax
`rtc.setAlarm(alarmType, seconds, minutes, hours, dayOrDate)`
##### Parameters
**alarmType:** A value from the alarmType above
**seconds:** The seconds value to set the alarm to. 
**minutes:** The minutes value to set the alarm to.  
**hours:** The hours value to set the alarm to.   
**dayOrDate:** The day of the week or the date of the month. 
##### Returns
None.
##### Example
```python
rtc = SDL_DS3231.SDL_DS3231(1, 0x68)
rtc.setAlarm(rtc.ALM1_MATCH_SECONDS, 5, 0, 0, 1)
```

### alarmInterrupt(self, alarmNumber, interruptEnabled)
##### Description
Enable or disable an alarm "interrupt". Note that this "interrupt" causes the RTC's INT pin to be asserted. To use this signal as an actual interrupt to a raspberry pi, it will need to be connected properly and programmed in the application firmware.
on the RTC.   
##### Syntax
`rtc.alarmInterrupt(alarmNumber, enable)`
##### Parameters
**alarmNumber:** The number of the alarm to enable or disable, ALARM_1 or ALARM_2
**alarmEnabled:** True or False
##### Returns
None.
##### Example
```python
rtc = SDL_DS3231.SDL_DS3231(1, 0x68)
rtc.alarmInterrupt(rtc.ALARM_1, True)      #assert the INT pin when Alarm1 occurs.
rtc.alarmInterrupt(rtc.ALARM_2, False)     #disable Alarm2
```

### alarm(self, alarmNumber)
##### Description
Tests whether an alarm has been triggered. If the alarm was triggered, returns true and resets the alarm flag in the RTC, else returns false.
##### Syntax
`rtc.alarm(alarmNumber)`
##### Parameters
**alarmNumber:** The number of the alarm to test, ALARM_1 or ALARM_2
##### Returns
Description *(type)*
##### Example
```python
rtc = SDL_DS3231.SDL_DS3231(1, 0x68)
if ( rtc.alarm(rtc.ALARM_1) ):		#has Alarm1 triggered?
	#yes, act on the alarm
else:
	#no alarm
```
### squareWave(self, freq)
##### Description
Enables or disables the square wave output.
##### Syntax
`rtc.squareWave(freq)`
##### Parameters
**freq:** a value from the freq above.
##### Returns
None.
##### Example
```python
rtc = SDL_DS3231.SDL_DS3231(1, 0x68)
rtc.squareWave(rtc.SQWAVE_1_HZ)	#1 Hz square wave
rtc.squareWave(rtc.SQWAVE_NONE)	#no square wave
```
### oscStopped(self, clearOSF)
##### Description
Returns the value of the oscillator stop flag (OSF) bit in the control/status register which indicates that the oscillator is or was stopped, and that the timekeeping data may be invalid. Optionally clears the OSF bit depending on the argument passed. If the `clearOSF` argument is omitted, the OSF bit is cleared by default. Calls to `set()` and `write()` also clear the OSF bit.

##### Syntax
`rtc.oscStopped(clearOSF)`
##### Parameters
**clearOSF:** an optional True or False value to indicate whether the OSF bit should be cleared (reset). If not supplied, a default value of true is used, resetting the OSF bit.
##### Returns
True or False
##### Example
```python
rtc = SDL_DS3231.SDL_DS3231(1, 0x68)
if ( rtc.oscStopped(False) ):		#check the oscillator
	#may be trouble
else:
	#all is well
```

# Arduino DS3232RTC Library Copyright by Jack Christensen
https://github.com/JChristensen/DS3232RTC  
README file  
Jack Christensen Mar 2013

![CC BY-SA](http://mirrors.creativecommons.org/presskit/buttons/80x15/png/by-sa.png)

# Original Copyright
SwitchDoc Labs, LLC  December 19, 2014

Clone respository and run testDS3231.py to test

More Information on www.switchdoc.com

Runs RTC and EEPROM


