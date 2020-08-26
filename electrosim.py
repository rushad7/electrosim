# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 20:25:08 2020

@author: Rushad
"""

import numpy as np

class Source():
    
    def __init__(self):
        self._t = np.arange(0, 20, 0.01)

    class CurrentSource():
        
        def __init__(self):
            pass
        
        def DC(self, current):
            self._Idc = current*np.ones(20)
        
        def AC(self, peak_current, angular_freq, phase_angle):        
            self._angular_freq = angular_freq
            self._phase_angle = phase_angle
            self._Iac = peak_current*np.sin(self.angular_freq*self.t + self.phase_angle)
    
    class VoltageSource():
        
        def __init__(self):
            pass
        
        def DC(self, voltage):
            self._Vdc = voltage*np.ones(20)
        
        def AC(self, peak_voltage, angular_freq, phase_angle):        
            self._angular_freq = angular_freq
            self._phase_angle = phase_angle
            self._Vac = peak_voltage*np.sin(self.angular_freq*self.t + self.phase_angle)
    
        
class Element():
    
    class resistor():
        def __init__(self, resistance):
            self.resistance = resistance

    class capacitor():
        def __init__(self, capacitance):
            self.capacitance = capacitance
        
    class inductor():
        def __init__(self, inductance):
            self.inductance = inductance