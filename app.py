#!/usr/bin/env python3

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
        QVBoxLayout, QWidget)

import os
import time
import GpioTester
import PinMappings as pinmap
import serial
import serial.tools.list_ports

BAUDRATE = 115200

def get_serial_ports():
    return serial.tools.list_ports.comports()

def set_serial_port():
    global gpioTester
    #TODO: change for windows later
    port = '/dev/ttyUSB0'
    gpioTester = GpioTester.GpioTester()
    gpioTester.init_board(BAUDRATE, port)

class ProductionFwGUI(QDialog):
    def check_conn(self):
        try:
            gpioTester
        except NameError:
            print("Error: Please select a COM port")
            return

    def __init__(self, parent=None):
        super(ProductionFwGUI, self).__init__(parent)

        # COM port select widgets
        comPortSelect = QComboBox(self)
        comPortSelect.addItem("Select")
        serial_ports = get_serial_ports()
        comPortSelect.addItems(map(str, serial_ports))
        comPortSelect.setFixedWidth(150)

        comPortLabel = QLabel("Select COM Port:")
        comPortLabel.setBuddy(comPortSelect)

        # GPIO widgets
        gpioSelect = QComboBox(self)
        gpioSelect.addItem("Select")
        gpioSelect.addItems(pinmap.getGpioList())
        gpioSelLabel = QLabel("Select GPIO:")
        gpioSelLabel.setBuddy(gpioSelect)
        gpioSelect.setFixedWidth(150)
       
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
        adcSelect.addItems(pinmap.getAdcList())
        adcSelLabel = QLabel("Select ADC:")
        adcSelLabel.setBuddy(gpioSelect)
        adcSelect.setFixedWidth(150)

        adcReadButton = QPushButton("Read")
        adcLineEdit = QLineEdit('')
        adcLineEdit.setReadOnly(True)

        # PWM widgets
        pwmSelect = QComboBox(self)
        pwmSelect.setFixedWidth(150)
        pwmSelect.addItem("Select")
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
        topLayout.setSpacing(10)
        topLayout.addStretch(1)

        row1Layout = QHBoxLayout()
        row1Layout.addWidget(gpioSelLabel)
        row1Layout.addWidget(gpioSelect)
        row1Layout.addWidget(gpioHighLowSelect)
        row1Layout.addWidget(gpioSetButton)
        row1Layout.addWidget(gpioReadButton)
        row1Layout.addWidget(gpioLineEdit)
        row1Layout.setSpacing(38)

        row2Layout = QHBoxLayout()
        row2Layout.addWidget(adcSelLabel)
        row2Layout.addWidget(adcSelect)
        row2Layout.addWidget(adcReadButton)
        row2Layout.addWidget(adcLineEdit)
        row2Layout.setSpacing(42)
        row2Layout.addStretch(1)

        row3Layout = QHBoxLayout()
        row3Layout.addWidget(pwmSelLabel)
        row3Layout.addWidget(pwmSelect)
        row3Layout.addWidget(pwmParamSelect)
        row3Layout.addWidget(pwmReadButton)
        row3Layout.addWidget(pwmReadLineEdit)
        row3Layout.addWidget(pwmSetButton)
        row3Layout.addWidget(pwmSetLineEdit)
        row3Layout.setSpacing(37)
        row3Layout.addStretch(1)
        
        mainLayout = QGridLayout()
        mainLayout.addLayout(topLayout,0,0)
        mainLayout.addLayout(row1Layout,1,0)
        mainLayout.addLayout(row2Layout,2,0)
        mainLayout.addLayout(row3Layout,3,0)
     
        self.setLayout(mainLayout)

        self.setWindowTitle("Production FW Interface")
        QApplication.setStyle(QStyleFactory.create('Fusion'))
        self.setFixedWidth(1000)
        self.setFixedHeight(250)

        self.setStyleSheet(open('main.qss').read())

        def set_gpio():
            #return 1 if self.check_conn() == 'None' else None
            net = str(gpioSelect.currentText())
            if (net == "Select"):
                print("Please select a GPIO pin")
                return
            pin = pinmap.getGpioMapping(net)
            value = 1 if gpioHighLowSelect.currentText() == 'High' else 0
            # TODO: clean this up
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
        
        def read_gpio():
            net = str(gpioSelect.currentText())
            if (net == "Select"):
                print("Please select a GPIO pin")
                return
            pin = pinmap.getGpioMapping(net)
            value = gpioTester.get_gpio(pin)
            gpioLineEdit.setText(value)
        
        def read_adc():
            net = str(adcSelect.currentText())
            if (net == "Select"):
                print("Please select an ADC")
                return
            channel = pinmap.getAdcMapping(net)
            value = gpioTester.get_adc(channel)
            adcLineEdit.setText(value)

        gpioSetButton.clicked.connect(set_gpio)
        gpioReadButton.clicked.connect(read_gpio)
        adcReadButton.clicked.connect(read_adc)
        comPortSelect.currentTextChanged.connect(set_serial_port)

if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    gallery = ProductionFwGUI()
    gallery.show()
    sys.exit(app.exec_()) 
