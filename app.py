#!/usr/bin/env python3

#Authors: Alex Lin, Justin Heimerl, Henry Roberts, Pedro Solares
#Purpose: The purpose of this file is to build and run the main GUI for the SONNEN FW interface.

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
        QVBoxLayout, QWidget, QFileDialog, QListView)
from PyQt5 import QtWidgets
import os
import time
import GpioTester
import PinMappings as pinmap
import serial
import serial.tools.list_ports
from datetime import datetime

from ScriptParser import ScriptParser

BAUDRATE = 115200

#Function: get_serial_ports()
#Arguments: None
#Return: List of serial ports available
#Purpose: Give list of serial ports to find the board.
def get_serial_ports():
    return serial.tools.list_ports.comports()

#Function: set_serial_ports()
#Arguments: Serial port object: port
#Return: None
#Purpose: Passes the correct port to the GPIO tester script.
def set_serial_port(port):
    global gpioTester
    gpioTester = GpioTester.GpioTester()
    gpioTester.init_board(BAUDRATE, port)

class ProductionFwGUI(QDialog):
    outputToTextFile = False
    outputFile = None

    def __init__(self, parent=None):
        super(ProductionFwGUI, self).__init__(parent)

        #STD output widget
        #self.le = QtWidgets.QLineEdit()

        self.te = QtWidgets.QTextEdit()
        clear_button = QPushButton("Clear")

        #Function:clear_text()
        #Arguments: none
        #Return: none
        #Purpose: Clear the textbox in the GUI.
        def clear_text():
            self.te.setText("")
        

        def getDateTime():
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            return dt_string

        
        #used to write outputs
        #Function:set_textbox(message)
        #Arguments: String called message.
        #Return: none
        #Purpose:Sets the textbox to contain the string as well as the data/time.
        def set_textbox(message):
            dt_string = getDateTime()
            self.te.setText(self.te.toPlainText()+"["+dt_string+"] "+message+"\n")
            #self.te.moveCursor.End()

        def handleFile():
            filePath = textFilePath.text()
            try:
                self.outputFile = open(filePath,'a+')
                self.outputToTextFile = True
                set_textbox("Output file path set to: "+filePath)
            except:
                set_textbox("Error: Invalid File Path")

        def stopWritingFile():
            try:
                if(self.outputToTextFile):
                    self.outputFile.close()
                    self.outputToTextFile = False
                    set_textbox("File closed successfully")
                else:
                    set_textbox("No file currently open")
            except:
                set_textbox("Error: No file set")

    
        #Text file select widgets
        textFileSelectLabel = QLabel("Output File Path:")
        textFilePath = QLineEdit('')
        textFilePath.setReadOnly(False)
        textPathSetButton = QPushButton("Set File Path")
        textPathCloseButton = QPushButton("Close Output File")

        # COM port select widgets
        comPortSelect = QComboBox(self)        
        comPortSelect.addItem("Select")
        serial_ports = get_serial_ports()
        comPortSelect.addItems(map(str, serial_ports))
        comPortSelect.setFixedWidth(150)

        comPortLabel = QLabel("Select COM Port:")
        comPortLabel.setBuddy(comPortSelect)

        scriptButton = QPushButton("Select Script...")

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
        pwmSelect.addItems(pinmap.getPwmList())
        pwmSelLabel = QLabel("Select PWM:")
        pwmSelLabel.setBuddy(gpioSelect)
        pwmParamSelect = QComboBox(self)
        pwmParamSelect.addItem("Control")
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
        topLayout.addWidget(scriptButton)

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

        row4Layout = QHBoxLayout()
        row4Layout.addWidget(textFileSelectLabel)
        row4Layout.addWidget(textFilePath)
        row4Layout.addWidget(textPathSetButton)
        row4Layout.addWidget(textPathCloseButton)


        row5Layout = QHBoxLayout()
        #row4Layout.addWidget(self.le)
        row5Layout.addWidget(self.te)
        row5Layout.addWidget(clear_button)

        mainLayout = QGridLayout()
        mainLayout.addLayout(topLayout,0,0)
        mainLayout.addLayout(row1Layout,1,0)
        mainLayout.addLayout(row2Layout,2,0)
        mainLayout.addLayout(row3Layout,3,0)
        mainLayout.addLayout(row4Layout,4,0)
        mainLayout.addLayout(row5Layout,5,0)
     
        self.setLayout(mainLayout)

        self.setWindowTitle("Production FW Interface")
        QApplication.setStyle(QStyleFactory.create('Fusion'))
        self.setFixedWidth(1000)
        self.setFixedHeight(550)

        self.setStyleSheet(open('main.qss').read())
        
        #Function:set_gpio()
        #Arguments: None
        #Return: None
        #Purpose: Tells the firmware to set the selected GPIO pin to the value in the value box.
        def set_gpio():
            try:
                gpioTester
            except NameError:
                set_textbox("Error: Please select a COM port")
                return
            net = str(gpioSelect.currentText())
            if (net == "Select"):
                set_textbox("Please select a GPIO pin")
                return
            pin = pinmap.getGpioMapping(net)
            value = 1 if gpioHighLowSelect.currentText() == 'High' else 0
            # TODO: clean this up
            if (pin == "Gpio21"):
                set_textbox("GPIO " + net + " is a relay")
                set_textbox("Signal: "+net)
                set_textbox("Set to: "+str(value))
                gpioTester.set_relay("AcK7", value)
                if(self.outputToTextFile):
                    self.outputFile.write(getDateTime())
                    self.outputFile.write(" w ")
                    self.outputFile.write("AcK7")
                    self.outputFile.write(" ")
                    self.outputFile.write(str(value))
                    self.outputFile.write("\n")
            elif (pin == "Gpio24"):
                set_textbox("GPIO " + pin + " is a relay")
                set_textbox("Signal: "+pin)
                set_textbox("Set to: "+str(value))
                gpioTester.set_relay("AcK5", value)
                if(self.outputToTextFile):
                    self.outputFile.write(getDateTime())
                    self.outputFile.write(" w ")
                    self.outputFile.write("AcK5")
                    self.outputFile.write(" ")
                    self.outputFile.write(str(value))
                    self.outputFile.write("\n")
            elif (pin == "Gpio25"):
                set_textbox("GPIO " + net + " is a relay")
                set_textbox("Signal: "+net)
                set_textbox("Set to: "+str(value))
                gpioTester.set_relay("AcK6", value)
                if(self.outputToTextFile):
                    self.outputFile.write(getDateTime())
                    self.outputFile.write(" w ")
                    self.outputFile.write("AcK6")
                    self.outputFile.write(" ")
                    self.outputFile.write(str(value))
                    self.outputFile.write("\n")
            elif (pin == "Gpio37"):
                set_textbox("GPIO " + net + " is a relay")
                set_textbox("Signal: "+net)
                set_textbox("Set to: "+str(value))
                gpioTester.set_relay("DcK1K2", value)
                if(self.outputToTextFile):
                    self.outputFile.write(getDateTime())
                    self.outputFile.write(" w ")
                    self.outputFile.write("DcK1K2")
                    self.outputFile.write(" ")
                    self.outputFile.write(str(value))
                    self.outputFile.write("\n")
            elif (pin == "Gpio49"):
                set_textbox("GPIO " + net + " is a relay")
                set_textbox("Signal: "+net)
                set_textbox("Set to: "+str(value))
                gpioTester.set_relay("AcK8", value)
                if(self.outputToTextFile):
                    self.outputFile.write(getDateTime())
                    self.outputFile.write(" w ")
                    self.outputFile.write("AcK8")
                    self.outputFile.write(" ")
                    self.outputFile.write(str(value))
                    self.outputFile.write("\n")
            else:
                gpioTester.set_gpio(pin, value)
                set_textbox("Signal: "+net)
                set_textbox("Set to: "+str(value))
                if(self.outputToTextFile):
                    self.outputFile.write(getDateTime())
                    self.outputFile.write(" w ")
                    self.outputFile.write(str(net))
                    self.outputFile.write(" ")
                    self.outputFile.write(str(value))
                    self.outputFile.write("\n")
        
        #Function: read_gpio()
        #Arguments: None
        #Return: None
        #Purpose: Prints the value of the selected GPIO to value box.
        def read_gpio():
            try:
                gpioTester
            except NameError:
                set_textbox("Error: Please select a COM port")
                return
            net = str(gpioSelect.currentText())
            if (net == "Select"):
                set_textbox("Please select a GPIO pin")
                return
            pin = pinmap.getGpioMapping(net)
            value = gpioTester.get_gpio(pin)
            set_textbox("Signal: "+net)
            set_textbox("Return: "+value)
            if(self.outputToTextFile):
                self.outputFile.write(getDateTime())
                self.outputFile.write(" r ")
                self.outputFile.write(net)
                self.outputFile.write(" ")
                self.outputFile.write(value)
                self.outputFile.write("\n")
            gpioLineEdit.setText(value)
        
        #Function: read_adc()
        #Arguments: None
        #Return: None
        #Purpose: Reads the selected ADC in the adcSelect box. Prints the value to the adcLineEdit box.
        def read_adc():
            try:
                gpioTester
            except NameError:
                set_textbox("Error: Please select a COM port")
                return
            net = str(adcSelect.currentText())
            if (net == "Select"):
                set_textbox("Please select an ADC")
                return
            channel = pinmap.getAdcMapping(net)
            value = gpioTester.get_adc(channel)
            set_textbox("Signal: "+net)
            set_textbox("Return: "+value)
            if(self.outputToTextFile):
                self.outputFile.write(getDateTime())
                self.outputFile.write(" r ")
                self.outputFile.write(net)
                self.outputFile.write(" ")
                self.outputFile.write(value)
                self.outputFile.write("\n")
            adcLineEdit.setText(value)

        #Function: set_pwm()
        #Arguments: None
        #Return: None
        #Purpose: Allows user to set various PWM parameters (many of these need to be implemented in GpioTester.py)
        def set_pwm():
            try:
                gpioTester
            except NameError:
                set_textbox("Error: Please select a COM port")
                return
            pwm = str(pwmSelect.currentText())
            if (pwm == "Select"):
                set_textbox("Please select a PWM")
                return
            mPwm = pinmap.getPwmMapping(pwm)
            param = str(pwmParamSelect.currentText())
            try:
                if (param == "Control"):
                    value = int(pwmSetLineEdit.text())
                    res = gpioTester.set_pwm(mPwm, value)
                elif (param == "Duty Cycle"):
                    value = int(pwmSetLineEdit.text())
                    res = gpioTester.set_pwmdutycycle(value)
                elif (param == "Frequency"):
                    value = int(pwmSetLineEdit.text())
                    res = gpioTester.set_pwmfrequency(value)
                set_textbox(res)
            except:
                set_textbox("PWM features unavailable in this revision.")

        #Function:read_pwm()
        #Arguments: None
        #Return: None
        #Purpose:Gives information about the selected PWM, not implemented correctly yet.
        def read_pwm():
            try:
                gpioTester
            except NameError:
                set_textbox("Error: Please select a COM port")
                return
            pwm = str(pwmSelect.currentText())
            if (pwm == "Select"):
                set_textbox("Please select a PWM")
                return
            try:
                mPwm = pinmap.getPwmMapping(pwm)
                param = str(pwmParamSelect.currentText())
            except:
                set_textbox("PWM features in development.")
            #TODO: finish this
        
        #Function: get_files()
        #Arguments: None
        #Return: none
        #Purpose: Allows the user to select a file to pass into the script parser.
        def get_files():
            try:
                gpioTester
            except NameError:
                set_textbox("Error: Please select a COM port")
                return
            parser = ScriptParser(gpioTester,self.outputToTextFile,self.outputFile)
            fname = QFileDialog.getOpenFileName(self, 'Open file', '~/',"Text files (*.txt)")
            parser.parseFile(str(fname[0]))
        
        #Function: set_com_port()
        #Arguments: None
        #Return: None
        #Purpose: Sets the COM port as selected. handles invalid COM ports gracefully (no crashing).
        def set_com_port():
            selected = str(comPortSelect.currentText())
            parsed = selected.split()
            port = parsed[0]
            try:
                set_serial_port(port)
                set_textbox("Serial connection established")
            except:
                set_textbox("Error: Invalid COM port")

        gpioSetButton.clicked.connect(set_gpio)
        gpioReadButton.clicked.connect(read_gpio)
        adcReadButton.clicked.connect(read_adc)
        pwmSetButton.clicked.connect(set_pwm)
        comPortSelect.currentTextChanged.connect(set_com_port)
        scriptButton.clicked.connect(get_files)
        textPathSetButton.clicked.connect(handleFile)
        textPathCloseButton.clicked.connect(stopWritingFile)
        clear_button.clicked.connect(clear_text)

if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    gallery = ProductionFwGUI()
    gallery = ProductionFwGUI()
    gallery.show()
    
    sys.exit(app.exec_())
    if(self.outputToTextFile):
        self.outputFile.close()
