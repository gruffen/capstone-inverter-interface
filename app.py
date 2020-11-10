#!/usr/bin/env python3

from PyQt5.QtCore import QDateTime, Qt, QTimer
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
        QVBoxLayout, QWidget)

import GpioTester
import os
import time
import serial
import serial.tools.list_ports

def serial_ports():
    return serial.tools.list_ports.comports()

def on_select(selected):
    global baudrate
    baudrate = 115200 # do not change
    global port
    port = selected[selected.find("(")+1:selected.find(")")]
    global gpioTester
    gpioTester = GpioTester.GpioTester()
    gpioTester.init_board(baudrate, port)

def set_gpio(pin, value):
    try:
        gpioTester
    except NameError:
        print("Error: Please select a COM port")
        return

    if (pin == "Gpio21"):
        print("GPIO " + pin + " is a relay")
        gpioTester.set_relay("AcK7", value)
    elif (pin == "Gpio24"):
        print("GPIO " + pin + " is a relay")
        gpioTester.set_relay("AcK5", value)
    elif (pin == "Gpio25"):
        print("GPIO " + pin + " is a relay")
        gpioTester.set_relay("AcK6", value)
    elif (pin == "Gpio37"):
        print("GPIO " + pin + " is a relay")
        gpioTester.set_relay("DcK1K2", value)
    elif (pin == "Gpio49"):
        print("GPIO " + pin + " is a relay")
        gpioTester.set_relay("AcK8", value)
    else:
        gpioTester.set_gpio(pin, value)

def read_gpio(pin):
    try:
        gpioTester
    except NameError:
        print("Error: Please select a COM port")
        return

    gpioTester.get_gpio(pin)

def read_adc(channel):
    try:
        gpioTester
    except NameError:
        print("Error: Please select a COM port")
        return
    
    gpioTester.get_adc(channel)


def set_pwm(pwm, value):
    try:
        gpioTester
    except NameError:
        print("Error: Please select a COM port")
        return

    gpioTester.set_pwm(pwm, value)

def set_pwmfrequency(value):
    try:
        gpioTester
    except NameError:
        print("Error: Please select a COM port")
        return

    gpioTester.set_pwmfrequency(value)

def get_pwmfrequency(pwm_frequency):
    try:
        gpioTester
    except NameError:
        print("Error: Please select a COM port")
        return

    gpioTester.get_pwmfrequency(pwm_frequency)


def set_pwmdutycycle(value):
    try:
        gpioTester
    except NameError:
        print("Error: Please select a COM port")
        return

    gpioTester.set_pwmdutycycle(value)


def get_pwmdutycycle(pwm_dutycycle):
    try:
        gpioTester
    except NameError:
        print("Error: Please select a COM port")
        return

    gpioTester.get_pwmdutycycle(pwm_dutycycle)

class ProductionFwGUI(QDialog):
    def __init__(self, parent=None):
        super(ProductionFwGUI, self).__init__(parent)

        # COM port select widgets
        comPortSelect = QComboBox(self)
        comPortSelect.addItem("Select")
        comPortSelect.addItem("COM0")
        comPortSelect.addItem("COM1")
        comPortSelect.addItem("COM2")
        comPortSelect.addItem("COM3")

        comPortLabel = QLabel("Select COM Port:")
        comPortLabel.setBuddy(comPortSelect)

        # GPIO widgets
        gpioSelect = QComboBox(self)
        gpioSelect.addItem("Select")
        gpioSelect.addItem("K5_Relay") # TODO: can make this a loop
        gpioSelect.addItem("COM1")
        gpioSelect.addItem("COM2")
        gpioSelect.addItem("COM3")
        gpioSelLabel = QLabel("Select GPIO:")
        gpioSelLabel.setBuddy(gpioSelect)

        gpioHighLowSelect = QComboBox(self)
        gpioHighLowSelect.addItem("High")
        gpioHighLowSelect.addItem("Low")
        gpioReadButton = QPushButton("Read")
        gpioSetButton = QPushButton("Set")
        gpioLineEdit = QLineEdit('')
        gpioLineEdit.setReadOnly(True)

        # ADC widgets
        adcSelect = QComboBox(self)
        adcSelect.addItem("Select")
        adcSelect.addItem("DC_Battery_Voltage")
        adcSelect.addItem("COM2")
        adcSelect.addItem("COM3")
        adcSelLabel = QLabel("Select ADC:")
        adcSelLabel.setBuddy(gpioSelect)

        adcReadButton = QPushButton("Read")
        adcLineEdit = QLineEdit('')
        adcLineEdit.setReadOnly(True)

        # PWM widgets
        pwmSelect = QComboBox(self)
        pwmSelect.addItem("PWM_DC")
        pwmSelect.addItem("COM1")
        pwmSelect.addItem("COM2")
        pwmSelect.addItem("COM3")
        pwmSelLabel = QLabel("Select PWM:")
        pwmSelLabel.setBuddy(gpioSelect)
        pwmParamSelect = QComboBox(self)
        pwmParamSelect.addItem("Duty Cycle") 
        pwmParamSelect.addItem("Frequency")

        pwmReadButton = QPushButton("Read")
        pwmReadLineEdit = QLineEdit('')
        pwmReadLineEdit.setReadOnly(True)

        pwmSetButton = QPushButton("Set")
        pwmSetLineEdit = QLineEdit('')

        #### LAYOUTS ####
        topLayout = QHBoxLayout()
        topLayout.addWidget(comPortLabel)
        topLayout.addWidget(comPortSelect)
        
        row1Layout = QHBoxLayout()
        row1Layout.addWidget(gpioSelLabel)
        row1Layout.addWidget(gpioSelect)
        row1Layout.addWidget(gpioHighLowSelect)
        row1Layout.addWidget(gpioSetButton)
        row1Layout.addWidget(gpioReadButton)
        row1Layout.addWidget(gpioLineEdit)

        row2Layout = QHBoxLayout()
        row2Layout.addWidget(adcSelLabel)
        row2Layout.addWidget(adcSelect)
        row2Layout.addWidget(adcReadButton)
        row2Layout.addWidget(adcLineEdit)

        row3Layout = QHBoxLayout()
        row3Layout.addWidget(pwmSelLabel)
        row3Layout.addWidget(pwmSelect)
        row3Layout.addWidget(pwmParamSelect)
        row3Layout.addWidget(pwmReadButton)
        row3Layout.addWidget(pwmReadLineEdit)
        row3Layout.addWidget(pwmSetButton)
        row3Layout.addWidget(pwmSetLineEdit)

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(topLayout)
        mainLayout.addLayout(row1Layout)
        mainLayout.addLayout(row2Layout)
        mainLayout.addLayout(row3Layout)
        self.setLayout(mainLayout)

        self.setWindowTitle("Production FW Interface")
        QApplication.setStyle(QStyleFactory.create('Fusion'))


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    gallery = ProductionFwGUI()
    gallery.show()
    sys.exit(app.exec_()) 
