import serial


class SerialConnector(object):
    def __init__(self):
        print("Amazon Tester")
        self.__ser = None

    def __del__(self):
        self.__close_connection();

    def init_board(self, baudrate, port, timeout):
        self.__ser = serial.Serial()
        self.__ser.baudrate = baudrate
        self.__ser.port = port
        self.__ser.timeout = timeout

        self.__ser.open()
        if self.__ser.is_open:
            print("serial connection established")
        else:
            print("serial connection failed!")

        self.readlines()

    def send_set_value_command(self, key, value):
        command = "Set:" + key + "=" + str(value) + "\n"
        self.__send_command(command)

    def send_get_value_command(self, key):
        command = "Get:" + key + "\n"
        self.__send_command(command)

    def send_write_gpio_command(self, key, value):
        command = "WriteIO:" + key + "=" + str(value) + "\n"
        self.__send_command(command)

    def send_read_gpio_command(self, key):
        command = "ReadIO:" + key + "\n"
        self.__send_command(command)

    def send_relay_command(self, relay, close):
        command = "Relay:" + relay + "=" + str(close) + "\n"
        self.__send_command(command)

    def send_get_adc_command(self, channel):
        command = "ADC:" + channel + "\n"
        self.__send_command(command)

    def send_set_pwm_command(self, pwm, enable):
        command = "PWM:" + pwm + "=" + str(enable) + "\n"
        self.__send_command(command)

    def send_set_pwmfrequency_command(self, value):
        command = "PWMConfig:" + "pwm_frequency" + "=" + str(value) + "\n"
        self.__send_command(command)

    def send_get_pwmfrequency_command(self, pwm_frequency):
        command = "PWMConfig:" + "pwm_frequency" + "=" + pwm_frequency + "\n"
        self.__send_command(command)

    def send_set_pwmdutycycle_command(self, value):
        command = "PWMConfig:" + "pwm_dutycycle" + "=" + str(value) + "\n"
        self.__send_command(command)

    def send_get_pwmdutycycle_command(self, pwm_dutycycle):
        command = "PWMConfig:" + "pwm_dutycycle" + "=" + pwm_dutycycle + "\n"
        self.__send_command(command)


    def readlines(self):
        result = ''
        array = self.__ser.readlines()
        for i in array:
            result = result + str(i.decode())
        return result

    def __send_command(self, command):
        self.__ser.write(command.encode())

    def __close_connection(self):
        self.__ser.close()
        print("serial connection closed")



