import SerialConnector
import time
import re

class GpioTester(object):

    def __init__(self):
        self.__serial = SerialConnector.SerialConnector()

    def init_board(self, baudrate, port, timeout=1):
        self.__serial.init_board(baudrate, port, timeout)

    def set_gpio(self, gpio, value):
        print("Set " + gpio.upper() + " = " + str(value))
        self.__serial.send_write_gpio_command(gpio, value)
        response = self.__serial.readlines()
        print("Response: " + str(response))

    def get_gpio(self, gpio):
        print("Get " + gpio.upper())
        self.__serial.send_read_gpio_command(gpio)
        response = self.__serial.readlines()
        print("Response: " + str(response))

        # get value of gpio
        value = re.search(r'\d+', str(response)).group()
        return value

        # This does not match the return format
        ########################################
        # if line.find("Pin enabled") != -1:
        #     print(gpio + " is 1")
        # elif line.find("Pin disabled") != -1:
        #     print(gpio + " is 0")
        # else:
        #     print("Error: " + line)
        #########################################

    def toggle_gpio(self, gpio, numbers, delay):
        for _ in range(numbers):
            self.set_gpio(gpio, 1)
            time.sleep(delay)
            self.set_gpio(gpio, 0)
            time.sleep(delay)

    def set_relay(self, relay, close):
        print("Relay " + relay + " = " + str(close))
        self.__serial.send_relay_command(relay, close)
        response = self.__serial.readlines()
        print("Response: " + str(response))

    def get_adc(self, channel):
        print("Get ADC channel " + str(channel))
        self.__serial.send_get_adc_command(channel)
        response = self.__serial.readlines()
        print("Response: " + str(response))

        values = re.findall(r'\d+', str(response))
        return values[2]

    def set_pwm(self, pwm, enable):
        print("Set " + pwm + " to " + ("disabled", "enabled")[enable])
        self.__serial.send_set_pwm_command(pwm, enable)
        response = self.__serial.readlines()
        print("Response: " + str(response))

        return str(response)

    def set_pwmfrequency(self, value):
        if value>=10000 and value<=80000:
            print("Set " + "pwm_frequency" + " = " + str(value))
            self.__serial.send_set_pwmfrequency_command(value)
            response = self.__serial.readlines()
            print("Response: " + str(response))
        else:
            print("Frequency should be between 10kHZ and 80kHZ")
        
        return str(response)

    def get_pwmfrequency(self, pwm_frequency):
        print("Get pwm_frequency =" + str(pwm_frequency))
        self.__serial.send_get_pwmfrequency_command(str(pwm_frequency))
        response = self.__serial.readlines()
        print("Response: " + str(response))

        values = re.findall(r'\d+', str(response))
        return str(response), values[1]

    def set_pwmdutycycle(self, value):
        if value >= 0 and value <= 100:
            print("Set " + "pwm_dutycycle" + " = " + str(value))
            self.__serial.send_set_pwmdutycycle_command(str(value))
            response = self.__serial.readlines()
            print("Response: " + str(response))
            return str(response)
        else:
            errortxt = "Dutycycle should be between 0 and 100"
            print(errortext)
            return errortxt

    def get_pwmdutycycle(self, pwm_dutycycle):
        print("Get pwm_dutycycle = " + str(pwm_dutycycle))
        self.__serial.send_get_pwmdutycycle_command(pwm_dutycycle)
        response = self.__serial.readlines()
        print("Response: " + str(response))

        values = re.findall(r'\d+', str(response))
        return str(response), values[1]

    @staticmethod
    def wait_any_key():
        input("Press enter to continue")
