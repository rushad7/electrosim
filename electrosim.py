# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 20:25:08 2020

@author: Rushad
"""

import numpy as np
        
class CurrentSource():
    
    class DC():
        def __init__(self, current):
            self._I = current*np.ones(len(np.arange(0, 20, 0.01)))
    
    class AC():        
        def __init__(self, peak_current, angular_freq, phase_angle):
            self._t = np.arange(0, 20, 0.01)
            self._angular_freq = angular_freq
            self._phase_angle = phase_angle
            self._I = peak_current*np.sin(self._angular_freq*self._t + self._phase_angle)
            
class VoltageSource():
    
    class DC():
        def __init__(self, voltage):
            self._V = voltage*np.ones(len(np.arange(0, 20, 0.01)))
    
    class AC():        
        def __init__(self, peak_voltage, angular_freq, phase_angle):
            self._t = np.arange(0, 20, 0.01)
            self._angular_freq = angular_freq
            self._phase_angle = phase_angle
            self._V = peak_voltage*np.sin(self._angular_freq*self._t + self._phase_angle)

class Element():
    
    class Resistor():
        
        def __init__(self, resistance):
            self._resistance = resistance

    class Capacitor():
        def __init__(self, capacitance):
            self.capacitance = capacitance
        
    class Inductor():
        def __init__(self, inductance):
            self.inductance = inductance
            
class Circuit():
    
    '''
    class Series():
        def __init__(self, element1, element2):
            self._element1 = element1
            self._element2 = element2
            
    class Parallel():
        def __init__(self, element1, element2):
            self._element1 = element1
            self._element2 = element2
      '''

    class Mesh():
        
        def __init__(self):
            self._node_voltage = []
            self._element_current = []
            self._temp_dict = {}
            
        def add(self, element, node1, node2):
            self._node1 = node1
            self._node2 = node2
            self._element = element
            
            # To add condition elem1 < > elem2
            if len(self._node_voltage) == 0 and len(self._node_voltage) == 0:
                
                if type(self._element) == CurrentSource.DC or type(self._element) == CurrentSource.AC:
                    self._temp_dict[str(self._node1) + str(self._node2)] = self._element._I
                    temp_dict_copy = self._temp_dict.copy()
                    self._element_current.append(temp_dict_copy)
                    self._temp_dict.clear()
                    
                    self._temp_dict[str(self._node1) + str(self._node2)] = None
                    temp_dict_copy = self._temp_dict.copy()
                    self._node_voltage.append(temp_dict_copy)
                    self._temp_dict.clear()
                    
                elif type(self._element) == VoltageSource.DC or type(self._element) == VoltageSource.AC:
                    self._temp_dict[str(self._node1) + str(self._node2)] = self._element._V
                    temp_dict_copy = self._temp_dict.copy()
                    self._node_voltage.append(temp_dict_copy)
                    self._temp_dict.clear()
                    
                    self._temp_dict[str(self._node1) + str(self._node2)] = None
                    temp_dict_copy = self._temp_dict.copy()
                    self._element_current.append(temp_dict_copy)
                    self._temp_dict.clear()
                
            if self._node_voltage[0]{'01'} != None:
                #vs
            elif self._element_current[0]{'01'} != None:
                #cs
                
                
            if type(self._element) == Element.Resistor:
                