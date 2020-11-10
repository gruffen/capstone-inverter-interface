###### Initialization ########################################
import GpioTester
import configparser
import os
import sys

# Read eeprom.ini file to get COM port
if os.path.isfile('./eeprom.ini'):
    config = configparser.ConfigParser()
    config.read('eeprom.ini')

    general = config['General']

    baudrate = general.getint('Baudrate', 115200)
    port = general.get('Port', 'COM7')

else:
    print("No ini file found")
    sys.exit(-1)

# Initialize GpioTester object
gpioTester = GpioTester.GpioTester()
gpioTester.init_board(baudrate, port)

###### End of Initialization #################################


###### Example commands ######################################

# This command is used to set a regular GPIO high or low.
# Pass as parameters the name of the pin, and 0 or 1 as a value.
# If the GPIO is intended to control a relay, you must use set_relay command (see below)
#
# C28 GPIOs:
# A.GPIO0 = "Gpio128"
# A.GPIO1 = "Gpio129"
# etc.
#
# Expected response:
# Set GPIO18 = 1
# Pin enabled
gpioTester.set_gpio("Gpio18", 1)


# This command is used to get the value of a GPIO
# Pass as a parameter the name of the pin
# C28 GPIOs begin with index "Gpio128" (corresponding to A.GPIO0)
#
# Expected response:
# Get GPIO30
# Response: Value = 0
gpioTester.get_gpio("Gpio30")


# This command is used to set a PWM output on a GPIO
# The following pins are assigned to Relays
# These pins cannot be set using the set_gpio command
#
# Gpio21 = "AcK7"
# Gpio24 = "AcK5"
# Gpio25 = "AcK6"
# Gpio37 = "DcK1K2"
# Gpio49 = "AcK8"
#
# Pass as parameters the name of the relay, and 0 or 1 as a value
# 1 corresponds to a PWM with 90% duty cycle, 0 is 0% duty cycle
#
# Expected Response:
# GPIO Gpio24 is a relay
# Relay AcK5 = 1
# Response: Relay AcK5 = 1
gpioTester.set_relay("AcK5", 1)


# This command is used to read the value of an ADC channel
# Pass as a parameter the name of the channel
# "ADCX_YY" where "X" is the ADC number ("1" or "2")
# and "YY" is the ADC channel ("A0", "B3", etc.)
#
# Expected output: (ADC register value 1510 and voltage 1.21V)
# Get ADC channel ADC1_A0
# Response: ,Raw Value, Input Value(x100V) =  1510, 121
gpioTester.get_adc("ADC1_A0")


# This command is used to enable or disable control PWM signals
# Pass as parameters the name of the PWM and a 0 or 1 to disable/enable
# "ePwmX" where "X" is the PWM number ("1" through "8")
# Default waveform is a 70% duty cycle at 20kHz
#
# Expected output:
# Response: 1Control PWMs handled by C28. Passing command...
# C28 Response: PWM enabled
gpioTester.set_pwm("ePwm1", 1)
