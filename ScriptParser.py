#!/usr/bin/env python3

import os
import time
import GpioTester
import PinMappings as pinmap

from tokenize import tokenize, untokenize, NUMBER, STRING, NAME, OP

class ScriptParser:
    state = "IDLE"
    gpioTester = None

    def __init__(self, mGpioTester):
        self.gpioTester = mGpioTester

    #Function: parseLine(self, line)
    #Arugment String called line.
    #Return: 0
    #Purpose: This function parses one line of the passed in text file to determine what command to pass
    #to the firmware. It is basically running a state machine.
    def parseLine(self, line):
        g = line.split()
        self.state = "IDLE"
        pin = None

        for tokval in g:
            if self.state == "IDLE":
                if tokval.lower() == "wait":
                    self.state = "WAIT_CMD"
                elif tokval.lower() == "read_gpio":
                    self.state = "GPIO_READ_CMD"
                elif tokval.lower() == "set_gpio":
                    self.state = "GPIO_SET_CMD"
                elif tokval.lower() == "read_adc":
                    self.state = "ADC_READ_CMD"
                elif tokval.lower() == "set_pwm_control":
                    self.state = "PWM_CSET_CMD"
                else:
                    print("Invalid command")
                    raise

            elif self.state == "WAIT_CMD":
                if (type(tokval) == int or float):
                    time.sleep(float(tokval))
                else:
                    print("Invalid argument for wait. Must be a number.")
                    raise

            elif self.state == "GPIO_READ_CMD":
                pin = pinmap.getGpioMapping(tokval)
                if (pin != None):
                    self.gpioTester.get_gpio(pin)
                else:
                    print("Invalid argument for GPIO read. Pin does not exist")
                    raise

            elif self.state == "GPIO_SET_CMD":
                pin = pinmap.getGpioMapping(tokval)
                if (pin != None):
                    self.state = "GPIO_SET_ARG"
                else:
                    print("Invalid argument for GPIO set. Pin does not exist")
                    raise

            elif self.state == "GPIO_SET_ARG":
                if (int(tokval) == 0 or int(tokval) == 1):
                    if (pin == "Gpio21"):
                        self.gpioTester.set_relay("AcK7", tokval)
                    elif (pin == "Gpio24"):
                        self.gpioTester.set_relay("AcK5", tokval)
                    elif (pin == "Gpio25"):
                        self.gpioTester.set_relay("AcK6", tokval)
                    elif (pin == "Gpio37"):
                        self.gpioTester.set_relay("DcK1K2", tokval)
                    elif (pin == "Gpio49"):
                        self.gpioTester.set_relay("AcK8", tokval)
                    else:
                        self.gpioTester.set_gpio(pin, value)
                else:
                    print("Invalid argument for GPIO set. Must be either 0 or 1.")
                    raise

            elif self.state == "ADC_READ_CMD":
                if (pinmap.getAdcMapping(tokval) != None):
                    self.gpioTester.read_adc(toknum)
                else:
                    print("Invalid argument for ADC read. Pin does not exist")
                    raise
            elif self.state == "PWM_CSET_CMD":
                pin = pinmap.getPwmMapping(tokval)
                if (pin != None):
                    self.state = "PWM_CSET_ARG"
                else:
                    print("Invalid argument for PWM control set. Pin does not exist")
                    raise

            elif self.state == "PWM_CSET_ARG":
                if (tokval == 0 or tokval == 1):
                    self.gpioTester.set_pwm(pin, tokval)
                else:
                    print("Invalid argument for PWM control set. Must be either 0 or 1.")
                    raise
            
            else:
                print("Invalid arguments")
                raise
        
        return 0

    #Function: parseFile(self, filename)
    #Argument: String called filename
    #Return: 0
    #Purpose: Function grabs each line of the input file to be parsed. 
    def parseFile(self, filename):
        with open(filename) as f:
            for line in f:
                ret = self.parseLine(line)
        
        return 0

if __name__ == '__main__':
    port = '/dev/ttyUSB0'
    BAUDRATE = 115200
    gpioTester = GpioTester.GpioTester()
    gpioTester.init_board(BAUDRATE, port)
    parser = ScriptParser(gpioTester)
    parser.parseFile("test_script.txt")
 
