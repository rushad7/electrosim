# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 20:25:08 2020

@author: Rushad
"""

import numpy as np
        
class CurrentSource():
    
    class DC():
        def __init__(self, current):
            self._t = np.arange(0, 20, 0.01)
            self._angular_freq = 0
            self._phase_angle = 0
            self._peak_current = current
            self._I = current*np.ones(len(self._t))
            self._V = None
    
    class AC():        
        def __init__(self, peak_current, angular_freq, phase_angle):
            self._t = np.arange(0, 20, 0.01)
            self._angular_freq = angular_freq
            self._phase_angle = phase_angle
            self._peak_current = peak_current
            self._I = self._peak_current*np.sin(self._angular_freq*self._t + self._phase_angle)
            self._V = None
            
class VoltageSource():
    
    class DC():
        def __init__(self, voltage):
            self._t = np.arange(0, 20, 0.01)
            self._angular_freq = 0
            self._phase_angle = 0
            self._peak_voltage = voltage
            self._V = voltage*np.ones(len(self._t))
            self._I = None
    
    class AC():        
        def __init__(self, peak_voltage, angular_freq, phase_angle):
            self._t = np.arange(0, 20, 0.01)
            self._angular_freq = angular_freq
            self._phase_angle = phase_angle
            self._peak_voltage = peak_voltage
            self._V = self._peak_voltage*np.sin(self._angular_freq*self._t + self._phase_angle)
            self._I = None

class Element():
    
    class Resistor():
        
        def __init__(self, resistance):
            self.resistance = resistance
            self._I = None
            self._V = None

    class Capacitor():
        def __init__(self, capacitance):
            self.capacitance = capacitance
            self._I = None
            self._V = None
        
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
            self._node = []
            self._temp_dict = {}
            self._element_index = 0
            
        def add(self, element, node1, node2):
            self._node1 = node1
            self._node2 = node2
            self._element = element
            
            # To add condition elem1 < > elem2
            #element_index 
            if len(self._node) == 0:
                self._temp_dict[str(self._node1) + str(self._node2)] = self._element
                temp_dict_copy = self._temp_dict.copy()
                self._node.append(temp_dict_copy)
                self._temp_dict.clear()
            else:
                self._temp_dict[str(self._node1) + str(self._node2)] = self._element
                temp_dict_copy = self._temp_dict.copy()
                self._node.append(temp_dict_copy)
                self._temp_dict.clear()
                self._element_index = self._element_index + 1

        def _getSource(self):
            
            if type(list(self._node[0].values())[0]) == CurrentSource.DC:
                source_type = 'cs'
            elif type(list(self._node[0].values())[0]) == CurrentSource.AC:
                source_type = 'cs'
            elif type(list(self._node[0].values())[0]) == VoltageSource.DC:
                source_type = 'vs'
            elif type(list(self._node[0].values())[0]) == VoltageSource.AC:
                source_type = 'vs'
            
            return source_type
            
        def solve(self):
            
            source_type = self._getSource()
            source = list(self._node[0].values())[0]
            
            if source_type == 'cs':
                self._I = source._I
                num_elem = len(self._node)
                total_impedance = 0
                
                for i in range(num_elem): 
                    
                    current_element = list(self._node[i].values())[0]
                    
                    if type(current_element) == Element.Resistor:
                        current_element._I = self._I
                        current_element._V = self._I*current_element.resistance
                        total_impedance = total_impedance + current_element.resistance
                        
                    elif type(current_element) == Element.Capacitor:
                        try:
                            impedance = 1/(source._angular_freq*current_element.capacitance)
                            current_element._I = self._I
                            current_element._V = (-1)*source._peak_current*impedance*np.cos(source._angular_freq*source._t + source._phase_angle)
                            total_impedance = total_impedance + impedance
                        except ZeroDivisionError:
                            current_element._I = self._I
                            current_element._V = (source._I*source._t)/current_element.capacitance
                            
                        
                    elif type(current_element) == Element.Inductor:
                        impedance = source.angular_freq*current_element.inductance
                        current_element._I = self._I
                        current_element._V = source._peak_current*impedance*np.cos(source._angular_freq*source._t + source._phase_angle)
                        total_impedance = total_impedance + impedance
                
                if type(current_element) == Element.Resistor:
                    source._V = (current_element._V*total_impedance)/current_element.resistance
                elif type(current_element) == Element.Capacitor:
                    source._V = (current_element._V*total_impedance)/current_element.capacitance
                elif type(current_element) == Element.Resistor:
                    source._V = (current_element._V*total_impedance)/current_element.inductance
                    