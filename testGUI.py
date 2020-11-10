import GpioTester
import os
import configparser
import time
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import serial
import serial.tools.list_ports

def serial_ports():
    return serial.tools.list_ports.comports()

def on_select(event = None):
    global baudrate
    baudrate = 115200 # do not change
    global port
    selected = cb.get()
    port = selected[selected.find("(")+1:selected.find(")")]
    global gpioTester
    gpioTester = GpioTester.GpioTester()
    gpioTester.init_board(baudrate, port)

def set_gpio(event = None):
    try:
        gpioTester
    except NameError:
        print("Error: Please select a COM port")
        return

    pin = s_g_pin_entry.get()
    value = s_g_value_entry.get()

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

def read_gpio(event = None):
    try:
        gpioTester
    except NameError:
        print("Error: Please select a COM port")
        return

    pin = g_g_pin_entry.get()
    gpioTester.get_gpio(pin)

def read_adc(event = None):
    try:
        gpioTester
    except NameError:
        print("Error: Please select a COM port")
        return

    channel = g_a_pin_entry.get()
    gpioTester.get_adc(channel)


def set_pwm(event = None):
    try:
        gpioTester
    except NameError:
        print("Error: Please select a COM port")
        return

    pwm = s_p_pwm_entry.get()
    value = int(s_p_value_entry.get())
    gpioTester.set_pwm(pwm, value)

def set_pwmfrequency(event = None):
    try:
        gpioTester
    except NameError:
        print("Error: Please select a COM port")
        return

    value = int(s_a_pwm_entry.get())
    gpioTester.set_pwmfrequency(value)

def get_pwmfrequency(event = None):
    try:
        gpioTester
    except NameError:
        print("Error: Please select a COM port")
        return

    pwm_frequency = s_a_pwm_entry.get()
    gpioTester.get_pwmfrequency(pwm_frequency)


def set_pwmdutycycle(event=None):
    try:
        gpioTester
    except NameError:
        print("Error: Please select a COM port")
        return

    value = int(s_g_pwm_entry.get())
    gpioTester.set_pwmdutycycle(value)


def get_pwmdutycycle(event=None):
    try:
        gpioTester
    except NameError:
        print("Error: Please select a COM port")
        return

    pwm_dutycycle = s_g_pwm_entry.get()
    gpioTester.get_pwmdutycycle(pwm_dutycycle)




"""Tkinter instance and Frame Creation"""
root = tk.Tk()
root.title("Amazon Production Testing")

""" Combobox with list of COM ports"""
l = tk.Label(text="Select a COM Port", borderwidth = 5, wraplength=250)
l.grid(row=0, column=5, padx=10, pady = 0, columnspan = 3)
cb = ttk.Combobox(values=serial_ports())
cb.grid(row=1, column=5, padx=10, pady = 0, columnspan = 3)
# assign function to combobox
cb.bind('<<ComboboxSelected>>', on_select)

vertical_spacer1 = tk.Label(text="___________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________")
vertical_spacer1.grid(row = 2, column = 0, padx = 5, pady = 0, columnspan = 12)


"""Set GPIO creation"""
s_g_main_label = tk.Label(text="SET A GPIO OR RELAY")
s_g_main_label.grid(row = 3, column = 0, padx = 10, pady = 30)

s_g_pin_label = tk.Label(text="Enter a Pin (format: Gpio18)")
s_g_pin_label.grid(row = 4, column = 0, padx = 10, pady = 0)

s_g_pin_entry = tk.Entry(borderwidth=4, relief="groove", background="white")
s_g_pin_entry.grid(row = 5, column = 0, padx = 10, pady = 0)

spacer1 = tk.Label(text="")
spacer1.grid(row = 6, column = 0, padx = 10, pady = 5)

s_g_value_label = tk.Label(text="Enter a Value for the Pin (0 or 1)")
s_g_value_label.grid(row = 7, column = 0, padx = 10, pady = 0)

s_g_value_entry = tk.Entry(borderwidth=4, relief="groove", background="white")
s_g_value_entry.grid(row = 8, column = 0, padx = 10, pady = 0)

spacer2 = tk.Label(text="")
spacer2.grid(row = 9, column = 0, padx = 10, pady = 2)

set_gpio_button = tk.Button(root, text="Set GPIO", command=set_gpio, fg="black", width=8)
set_gpio_button.grid(row=10, column=0, padx=10, pady=10)

horizontal_spacer1 = tk.Label(text="\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n", background = "black")
horizontal_spacer1.grid(row = 3, column = 1, padx = 5, pady = 0, rowspan=8)


"""Get GPIO creation"""
g_g_main_label = tk.Label(text="GET A GPIO")
g_g_main_label.grid(row = 3, column = 2, padx = 10, pady = 30)

g_g_pin_label = tk.Label(text="Enter a Pin (format: Gpio16)")
g_g_pin_label.grid(row = 4, column = 2, padx = 10, pady = 0)

g_g_pin_entry = tk.Entry(borderwidth=4, relief="groove", background="white")
g_g_pin_entry.grid(row = 5, column = 2, padx = 10, pady = 0)

get_gpio_button = tk.Button(root, text="Read GPIO", command=read_gpio, fg="black", width=8)
get_gpio_button.grid(row=10, column=2, padx=10, pady=10)


horizontal_spacer2 = tk.Label(text="\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n", background = "black")
horizontal_spacer2.grid(row = 3, column = 3, padx = 5, pady = 5, rowspan=8)



"""Get ADC creation"""
g_a_main_label = tk.Label(text="GET AN ADC")
g_a_main_label.grid(row = 3, column = 4, padx = 10, pady = 30)

g_a_pin_label = tk.Label(text="Enter an ADC (format: ADC1_A0)")
g_a_pin_label.grid(row = 4, column = 4, padx = 10, pady = 0)

g_a_pin_entry = tk.Entry(borderwidth=4, relief="groove", background="white")
g_a_pin_entry.grid(row = 5, column = 4, padx = 10, pady = 0)

get_adc_button = tk.Button(root, text="Read ADC", command=read_adc, fg="black", width=8)
get_adc_button.grid(row=10, column=4, padx=10, pady=10)

horizontal_spacer3 = tk.Label(text="\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n", background = "black")
horizontal_spacer3.grid(row = 3, column = 5, padx = 5, pady = 0, rowspan=8)


"""Set PWM creation"""
s_p_main_label = tk.Label(text="SET A CONTROL PWM")
s_p_main_label.grid(row = 3, column = 6, padx = 10, pady = 30)

s_p_pwm_label = tk.Label(text="Enter a PWM (format: ePwm1)")
s_p_pwm_label.grid(row = 4, column = 6, padx = 10, pady = 0)

s_p_pwm_entry = tk.Entry(borderwidth=4, relief="groove", background="white")
s_p_pwm_entry.grid(row = 5, column = 6, padx = 10, pady = 0)

spacer3 = tk.Label(text="")
spacer3.grid(row = 6, column = 6, padx = 10, pady = 5)

s_p_value_label = tk.Label(text="Enter a value for the PWM (0 or 1)")
s_p_value_label.grid(row = 7, column = 6, padx = 10, pady = 0)

s_p_value_entry = tk.Entry(borderwidth=4, relief="groove", background="white")
s_p_value_entry.grid(row = 8, column = 6, padx = 10, pady = 0)

spacer4 = tk.Label(text="")
spacer4.grid(row = 9, column = 6, padx = 10, pady = 2)

set_pwm_button = tk.Button(root, text="Set PWM", command=set_pwm, fg="black", width=8)
set_pwm_button.grid(row=10, column=6, padx=10, pady=10)

horizontal_spacer3 = tk.Label(text="\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n", background = "black")
horizontal_spacer3.grid(row = 3, column = 7, padx = 5, pady = 0, rowspan=8)

"""PWM Frequency creation"""
s_a_main_label = tk.Label(text="Set PWM Frequency")
s_a_main_label.grid(row = 3, column = 8, padx = 10, pady = 30)

s_a_pwm_label = tk.Label(text="Enter a value for the PWM Frequency (10kHZ to 80 kHZ)")
s_a_pwm_label.grid(row = 4, column = 8, padx = 10, pady = 0)

s_a_pwm_entry = tk.Entry(borderwidth=4, relief="groove", background="white")
s_a_pwm_entry.grid(row = 5, column = 8, padx = 10, pady = 0)

spacer3 = tk.Label(text="")
spacer3.grid(row = 6, column = 8, padx = 10, pady = 5)

set_pwm_button = tk.Button(root, text="Set PWM", command=set_pwmfrequency, fg="black", width=8)
set_pwm_button.grid(row=7, column=8, padx=10, pady=10)

s_a_main_label = tk.Label(text="Get PWM Frequency")
s_a_main_label.grid(row = 8, column = 8, padx = 10, pady = 30)

set_pwm_button = tk.Button(root, text="Get PWM", command=get_pwmfrequency, fg="black", width=8)
set_pwm_button.grid(row=9, column=8, padx=10, pady=10)

horizontal_spacer3 = tk.Label(text="\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n", background = "black")
horizontal_spacer3.grid(row = 3, column = 9, padx = 5, pady = 0, rowspan=8)

"""PWM Duty Cycle creation"""
s_g_main_label = tk.Label(text="Set PWM Duty Cycle")
s_g_main_label.grid(row = 3, column = 10, padx = 10, pady = 30)

s_g_pwm_label = tk.Label(text="Enter a value for the PWM Duty Cycle (0 to 100)")
s_g_pwm_label.grid(row = 4, column = 10, padx = 10, pady = 0)

s_g_pwm_entry = tk.Entry(borderwidth=4, relief="groove", background="white")
s_g_pwm_entry.grid(row = 5, column = 10, padx = 10, pady = 0)

spacer3 = tk.Label(text="")
spacer3.grid(row = 6, column = 10, padx = 10, pady = 5)

set_pwm_button = tk.Button(root, text="Set PWM", command=set_pwmdutycycle, fg="black", width=8)
set_pwm_button.grid(row=7, column=10, padx=10, pady=10)

s_g_main_label = tk.Label(text="Get PWM Duty Cycle")
s_g_main_label.grid(row = 8, column = 10, padx = 10, pady = 30)

set_pwm_button = tk.Button(root, text="Get PWM", command=get_pwmdutycycle, fg="black", width=8)
set_pwm_button.grid(row=9, column=10, padx=10, pady=10)


root.mainloop()

