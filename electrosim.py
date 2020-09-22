# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 20:25:08 2020

@author: Rushad
"""

import numpy as np
import sympy  
      
class CurrentSource():
    
    class DC():
        def __init__(self, current, name):
            self._t = np.arange(0, 20, 0.01)
            self._I = current
            self._name = sympy.core.symbols(name)
    
    class AC():        
        def __init__(self, peak_current, angular_freq, phase_angle, name):
            self._t = sympy.core.symbols('t')
            self._angular_freq = angular_freq
            self._phase_angle = phase_angle
            self._I = peak_current*sympy.sin(self._angular_freq*self._t + self._phase_angle)
            self._name = sympy.core.symbols(name)
            
class VoltageSource():
    
    class DC():
        def __init__(self, voltage, name):
            self._t = np.arange(0, 20, 0.01)
            self._V = voltage*np.ones(len(self._t))
            self._name = sympy.core.symbols(name)
    
    class AC():        
        def __init__(self, peak_voltage, angular_freq, phase_angle, name):
            self._t = sympy.core.symbols('t')
            self._angular_freq = angular_freq
            self._phase_angle = phase_angle
            self._V = peak_voltage*sympy.sin(self._angular_freq*self._t + self._phase_angle)
            self._name = sympy.core.symbols(name)

class Element():
    
    class Resistor():
        
        def __init__(self, resistance, name):
            self.property = resistance
            self._name = sympy.core.symbols(name)

    class Capacitor():
        def __init__(self, capacitance, name):
            self.property = capacitance
            name = "X" + str(name)
            self._name = sympy.core.symbols(name)
        
    class Inductor():
        def __init__(self, inductance, name):
            self.property = inductance
            name = "X" + str(name)
            self._name = sympy.core.symbols(name)
            
class Circuit():

    class Mesh():
        
        def __init__(self):
            self._node = []
            self._temp_dict = {}
            self._element_index = 0
            
        def add(self, element, node1, node2):
            self._node1 = node1
            self._node2 = node2
            self._element = element
            
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
        
        def _checkMesh(self):
            
            for i in range(len(self._node)):
                if i != len(self._node) -1:
                    if int(list(self._node[i].keys())[0][1]) == int(list(self._node[i+1].keys())[0][0]):
                        check = True 
                    else:
                        print('Mesh continuity is broken. Check node values before solving')
                        check = False
                else:
                    if int(list(self._node[i].keys())[0][1]) == int(list(self._node[0].keys())[0][0]):
                        check = True
                    else:
                        print('Mesh continuity is broken. Check node values before solving')
                        check = False
                
            return check
        
        def solve(self):
            check = self._checkMesh()
            if check == True:
                solution_value = self._solver()
                return solution_value
            else:
                pass
        
        def _solver(self):
            
            source = self._getSource()
            if source == 'cs':
                    
                temp_eq = 0
                temp_eq_list = []
                eq_list = []
                
                for i in range(len(self._node)):
                    current_node = (list(self._node[i].keys())[0][0], list(self._node[i].keys())[0][1])
                    current_node_ep = current_node[1]
                    
                    for j in range(len(self._node)):
                        next_node = (list(self._node[j].keys())[0][0], list(self._node[j].keys())[0][1])
                        next_node_sp = next_node[0]
                        
                        if current_node_ep == next_node_sp:
                            
                            if type(list(self._node[i].values())[0]) == CurrentSource.DC or type(list(self._node[i].values())[0]) == CurrentSource.AC:
                                temp_eq = temp_eq + list(self._node[i].values())[0]._I
                                temp_eq_list.append(temp_eq)
                                temp_eq = 0
                            else:   
                                node1 = 'V' + str(current_node[0])
                                node2 = 'V' + str(current_node[1])
                                
                                node1 = sympy.core.symbols(node1)
                                node2 = sympy.core.symbols(node2)
                                
                                impedance = list(self._node[i].values())[0].property
                                temp_eq  = temp_eq + (node1 - node2)/impedance
                                temp_eq_list.append(temp_eq)
                                temp_eq = 0
            
            for i in range(len(temp_eq_list)):
                if i == len(temp_eq_list)-1:
                    eq_list.append(sympy.Eq(temp_eq_list[i], temp_eq_list[0]))
                else:
                    eq_list.append(sympy.Eq(temp_eq_list[i], temp_eq_list[i+1]))
            
            var_list = [sympy.core.symbols("V" + str(i)) for i in range(len(self._node))]
            var_tuple = tuple(var_list)
            solution = sympy.linsolve(eq_list, var_tuple)
            
            last_node_eq = 0
            solution_args = solution.args[0]
            
            for i in range(len(solution_args)):
                last_node_eq = last_node_eq + solution_args[i]
            
            last_node_value = sympy.solve(last_node_eq)[0]
            last_node_var = sympy.core.symbols('V' + str(len(self._node)-1))
            
            if type(last_node_value) == dict:
                last_node_value = last_node_value[last_node_var]
                solution_value = solution.subs(last_node_var, last_node_value)
                solution_value = solution_value.args
                solution_value = solution_value[0]
                pass
            else:
                solution_value = solution.subs(last_node_var, last_node_value)
                solution_value = solution_value.args
                solution_value = solution_value[0]
            
            return solution_value