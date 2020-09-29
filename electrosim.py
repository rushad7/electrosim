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
            self._angular_freq = 0
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
            self._angular_freq = 0.0001
            self._V = voltage
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
            
        def add(self, element, node1, node2):
            
            if len(self._node) == 0:
                self._temp_dict[str(node1) + str(node2)] = element
                temp_dict_copy = self._temp_dict.copy()
                self._node.append(temp_dict_copy)
                self._temp_dict.clear()
            else:
                self._temp_dict[str(node1) + str(node2)] = element
                temp_dict_copy = self._temp_dict.copy()
                self._node.append(temp_dict_copy)
                self._temp_dict.clear()

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
        
        def checkMesh(self, ret=False, disp=True):
            
            if type(list(self._node[0].values())[0]) == CurrentSource.DC or type(list(self._node[0].values())[0]) == CurrentSource.AC or type(list(self._node[0].values())[0]) == VoltageSource.DC or type(list(self._node[0].values())[0]) == VoltageSource.AC:
                for i in range(len(self._node)):
                    
                    if i != len(self._node) -1:
                        if int(list(self._node[i].keys())[0][1]) == int(list(self._node[i+1].keys())[0][0]):
                            check = True 
                        else:
                            check = False
                            
                    else:
                        if int(list(self._node[i].keys())[0][1]) == int(list(self._node[0].keys())[0][0]):
                            check = True
                        else:
                            check = False
                    
                    if check == False:
                        break
                            
                if check == True:
                    if disp == True:
                        if int(list(self._node[0].keys())[0][0]) == 0 and int(list(self._node[-1].keys())[0][1]) == 0:
                            print('Mesh continuity is intact')
                        else:
                            print('Mesh starting from non zero node')
                else:
                    print('Mesh continuity is broken. Check nodes before solving')
                
                if ret == True:
                    return check
            else:
                if disp == True:
                    print('Make sure node 0-1 is always a source')
        
        def _solver(self):
            
            def solverCS():
                        
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
                                
                                impedance = list(self._node[i].values())[0].property*list(self._node[0].values())[0]._angular_freq
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
            
            def solverVS():
                
                temp_eq = 0
                temp_eq_list = []
                
                impdedance_total = self.impedance()
                current_total = (list(self._node[0].values())[0]._V)/impdedance_total
                
                for i in range(len(self._node)):
                    current_node = (list(self._node[i].keys())[0][0], list(self._node[i].keys())[0][1])
                    current_node_ep = current_node[1]
                    
                    for j in range(len(self._node)):
                        next_node = (list(self._node[j].keys())[0][0], list(self._node[j].keys())[0][1])
                        next_node_sp = next_node[0]
                        
                        if current_node_ep == next_node_sp:
                            
                            if type(list(self._node[i].values())[0]) == VoltageSource.DC or type(list(self._node[i].values())[0]) == VoltageSource.AC:
                                
                                node1 = 'V' + str(current_node[0])
                                node2 = 'V' + str(current_node[1])
                                
                                node1 = sympy.core.symbols(node1)
                                node2 = sympy.core.symbols(node2)
                                
                                temp_eq  = temp_eq + node1 - node2 - list(self._node[0].values())[0]._V
                                temp_eq_list.append(temp_eq)
                                temp_eq = 0
                                
                            else:   
                                node1 = 'V' + str(current_node[0])
                                node2 = 'V' + str(current_node[1])
                                
                                node1 = sympy.core.symbols(node1)
                                node2 = sympy.core.symbols(node2)
                                
                                t = sympy.core.symbols('t')
                                
                                if type(list(self._node[i].values())[0]) == Element.Resistor:    
                                    temp_eq  = temp_eq + node1 - node2 - current_total*list(self._node[i].values())[0].property
                                elif type(list(self._node[i].values())[0]) == Element.Capacitor:
                                    xc = 1/(list(self._node[i].values())[0].property*list(self._node[0].values())[0]._angular_freq)
                                    temp_eq  = temp_eq + node1 - node2 - sympy.integrate(current_total,t)*xc
                                elif type(list(self._node[i].values())[0]) == Element.Inductor:
                                    xl = list(self._node[i].values())[0].property*list(self._node[0].values())[0]._angular_freq
                                    temp_eq  = temp_eq + node1 - node2 - ((sympy.integrate(current_total,t)*xl)/(2*np.pi))
                                
                                temp_eq_list.append(temp_eq)
                                temp_eq = 0
                
                var_list = [sympy.core.symbols("V" + str(i)) for i in range(len(self._node))]
                var_tuple = tuple(var_list)
                
                if type(list(self._node[0].values())[0]) == VoltageSource.AC: 
                    for i in range(len(self._node)):
                        eq_ordered_list = temp_eq_list[i].as_ordered_terms()
                        temp_eq = (eq_ordered_list[0] + eq_ordered_list[1])/(eq_ordered_list[2].args[0])
                        temp_eq_list[i] = temp_eq
                    '''
                    solution = sympy.linsolve(temp_eq_list, var_tuple)
                    solution = solution.args[0]
                    solution_sum = sum(solution)
                    last_var_value = list(self._node[0].values())[0]._V/solution_sum.args[0]
                    solution = solution.subs(var_tuple[-1], last_var_value)
                    '''
                else:
                    var_list.append(sympy.core.symbols('t'))
                    var_tuple = tuple(var_list)
                    solution = sympy.linsolve(temp_eq_list, var_tuple)
                    solution = solution.args[0]
                    last_var_value = sympy.solve(sum(solution))[0]
                    solution = solution.subs(var_tuple[-2], last_var_value)
                
                return temp_eq_list, var_tuple
            
            
            source = self._getSource()
            if source == 'cs':
                solution_value = solverCS()
                return solution_value
            
            elif source == 'vs':
                solution_value = solverVS()
                return solution_value
                

        def solve(self):
            check = self.checkMesh(ret=True, disp=False)
            if check == True:
                solution_value = self._solver()
                return solution_value
            else:
                print('Check Mesh node continuity')

        def impedance(self, across_node=(0,1)):
            
            r = 0
            xc = 0
            xl = 0
            
            for i in range(1, len(self._node)):
                
                if type(list(self._node[i].values())[0]) == Element.Resistor:
                    r = r + list(self._node[i].values())[0].property
                elif type(list(self._node[i].values())[0]) == Element.Capacitor:
                    xc = xc + 1/(list(self._node[i].values())[0].property*list(self._node[0].values())[0]._angular_freq)
                elif type(list(self._node[i].values())[0]) == Element.Inductor:
                    xl = xl + list(self._node[i].values())[0].property*list(self._node[0].values())[0]._angular_freq
            
            if across_node != (0,1):
                
                impedance_across_element = self._node[across_node[0]][str(across_node[0])+str(across_node[1])]
                
                if type(impedance_across_element) == Element.Resistor:
                    r_across = list(self._node[across_node[0]].values())[0].property
                    r = r - r_across
                elif type(impedance_across_element) == Element.Capacitor:
                    xc_across = 1/(list(self._node[across_node[0]].values())[0].property*list(self._node[0].values())[0]._angular_freq)
                    xc = xc - xc_across
                elif type(impedance_across_element) == Element.Inductor:
                    xl_across = list(self._node[across_node[0]].values())[0].property*list(self._node[0].values())[0]._angular_freq
                    xl = xl - xl_across
            
            impedance = np.sqrt(r**2 + (xl-xc)**2)
            return impedance