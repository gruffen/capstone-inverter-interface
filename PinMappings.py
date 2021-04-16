#!/usr/bin/env python3

gpioMapping = {
    'Fault_Sig4': 'Gpio16',
    '24BAT_EN': 'Gpio18',
    'Fault_Sig5': 'Gpio20',
    'K7_Relay': 'Gpio21',
    'RLY_TST_uC': 'Gpio22',
    'Fault_Sig3': 'Gpio23',
    'K5_Relay': 'Gpio24',
    'K6_Relay': 'Gpio25',
    'K_DC_precharge1': 'Gpio26',
    'K_DC_precharge2': 'Gpio27',
    'GF_6': 'Gpio36',
    'K_DC_Main': 'Gpio37',
    'DEMAG': 'Gpio48',
    'K8_Relay': 'Gpio49',
    'GF_30': 'Gpio50',
    'M3_AC_PWM_EN': 'Gpio51',
    'N_PE_Fail': 'Gpio54',
    'GO-SUPPLY-ERROR': 'Gpio55',
    'GF_Err': 'Gpio56',
    'Fault_Sig1': 'Gpio57',
    'Fault_Sig3': 'Gpio58',
    'M3_DC_PWM_EN': 'Gpio59',
    'EXT-ATS1': 'Gpio60',
    'EXT-ATS2': 'Gpio61',
    'EXT-DI2': 'Gpio62',
    'EXT-DI1': 'Gpio63',
    'GF-PWM': 'Gpio68',
    'K_DC_Main_C28': 'Gpio129',
    'C28_AC_Relay_Sfty_EN': 'Gpio128',
    'MOD_CMP': 'Gpio2',
    'RCD_TRIP_C28': 'Gpio3'
}

adcMapping = {
    'V_AC_L1': 'ADC1_A0',
    'Dc_Input_Voltage': 'ADC1_A2',
    'I_AC_L1_Grid': 'ADC1_A3',
    'DcLink_Voltage': 'ADC1_A4',
    '+BUS_MP': 'ADC1_A6',
    'I_DC_Leg1': 'ADC1_A7',
    'IGBT_AC_L2_Temp': 'ADC1_B0',
    'DC_CHOKE_Temp': 'ADC1_B3',
    'V_AC_L2': 'ADC1_B4',
    'I_AC_L2_Grid': 'ADC1_B7',
    '1.5VREF_DSP': 'ADC2_A0',
    'I_DC_Leg2': 'ADC2_A2',
    'IGBT_DC_Temp': 'ADC2_A3',
    'Board_Temp': 'ADC2_A6',
    'I_AC_L2_Inverter': 'ADC2_A7',
    '-BUS_MP': 'ADC2_B0',
    'I_AC_L1_Inverter': 'ADC2_B3',
    'DC_Battery_Voltage': 'ADC2_B4',
    'V_AC_L1_GridTerminal': 'ADC2_B7'
}

pwmMapping = {
    'PWM1': 'ePwm1',
    'PWM2': 'ePwm2',
    'PWM3': 'ePwm3',
    'PWM4': 'ePwm4',
    'PWM5': 'ePwm5',
    'PWM6': 'ePwm6',
    'PWM7': 'ePwm7',
    'PWM8': 'ePwm8'
}

def getGpioList():
    return list(gpioMapping.keys())

def getGpioMapping(key):
    return gpioMapping.get(str(key))

def getAdcList():
    return list(adcMapping.keys())

def getAdcMapping(key):
    return adcMapping.get(str(key))

def getPwmList():
    return list(pwmMapping.keys())

def getPwmMapping(key):
    return pwmMapping.get(str(key))

if __name__ == '__main__':
    print(gpioMapping)