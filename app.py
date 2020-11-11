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
        comPortSelect.setFixedWidth(150)


        comPortLabel = QLabel("Select COM Port:")
        comPortLabel.setBuddy(comPortSelect)

        # GPIO widgets
        gpioSelect = QComboBox(self)
        gpioSelect.addItem("Select")
        gpioSelect.addItem("K5_Relay")
        gpioSelect.addItem("COM1")
        gpioSelect.addItem("COM2")
        gpioSelect.addItem("COM3")
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
        adcSelect.addItem("DC_Battery_Voltage")
        adcSelect.addItem("COM2")
        adcSelect.addItem("COM3")
        adcSelLabel = QLabel("Select ADC:")
        adcSelLabel.setBuddy(gpioSelect)
        adcSelect.setFixedWidth(150)

        adcReadButton = QPushButton("Read")
        adcLineEdit = QLineEdit('')
        adcLineEdit.setReadOnly(True)

        # PWM widgets
        pwmSelect = QComboBox(self)
        pwmSelect.setFixedWidth(150)
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


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    gallery = ProductionFwGUI()
    gallery.show()
    sys.exit(app.exec_()) 
