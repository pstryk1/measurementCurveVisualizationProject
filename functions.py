from math import pi
import dataVar as dV
"""
def check_float(element):

    '''
    Checks if the given argument can be converted to float.
    Returns the converted argument.
    '''
    
    while True:
        try:
            element = float(element)
            break
        except ValueError:
            element = input(f'Inproper value. Please try again: ')
    return element


def check(element, conditions, type):

    '''
    Checks if the given argument meets the given conditions.
    '''

    if type == 'choice':
        while element not in conditions:
            element = input('Inproper value. Please try again: ')
    elif type == 'range':
        while element <= conditions[0] or element > conditions[len(conditions)-1]:
            element = check_float(input('Inproper value. Please try again: '))
    return element
"""

class measurement:

    def __init__(self, system):

        '''
        Creates an object of the measurement class based on the chosen measurement system.
        "Układ Wennera", "Układ Schlumbergera", "Układ Trójelektrodowy"
        '''
        self.system = dV.mes_system
        
        if self.system == 'Układ Wennera':
            self.ambn = dV.distance1
            self.mn = self.ambn
            self.a_position = 0
            self.b_position = 3*self.ambn
            self.m_position = self.ambn
            self.n_position = 2*self.ambn
            self.middle = self.ambn+self.ambn/2
            self.distance1 = self.ambn
            self.distance2 = 2*self.ambn
            self.geometry_factor = pi*2*self.ambn

        elif self.system == 'Układ Schlumbergera':
            self.ambn = dV.distance1
            self.mn = dV.distance2
            self.a_position = 0
            self.b_position = 2*self.ambn+self.mn
            self.m_position = self.ambn
            self.n_position = self.ambn+self.mn
            self.middle = self.ambn+self.mn/2
            self.distance1 = self.ambn
            self.distance2 = self.ambn+self.mn
            self.geometry_factor = pi*self.ambn*(self.ambn+self.mn)/self.mn

        else:
            self.ambn = dV.distance1
            self.mn = dV.distance2
            
            if dV.variant == 'Forward':
                self.a_position = 0
                self.b_position = None
                self.m_position = self.ambn
                self.n_position = self.ambn+self.mn
                self.middle = self.ambn+self.mn/2
            else:
                self.a_position = None
                self.b_position = self.mn+self.ambn
                self.m_position = 0
                self.n_position = self.mn
                self.middle = self.mn/2

            self.distance1 = self.ambn
            self.distance2 = self.ambn+self.mn
            self.geometry_factor = 2*pi*self.ambn*(self.ambn+self.mn)/self.mn

            
    def measure(self, system, x_delta, env_data):

        '''
        Calculates the apparent resistivity for all of the point on a 2D profile of a two layer model.
        '''

        def check_side(e, r):

            '''
            Checks if the emitter and reciever electrodes are placed on the same layer.
            '''

            if (e <= 50 and r <= 50):
                return [True, 0, 0]
            elif (e >= 50 and r >= 50):
                return [True, 1, 1]
            elif (e < 50 and r > 50):
                return [False, 0, 1]
            elif (e > 50 and r < 50):
                return [False, 1, 0]

            
        def distance_prim(e, r):

            '''
            Calculates the distance between the reciever and the reflection point of emitter.
            '''

            if e < 50:
                return abs(50+(50-e)-r)
            else:
                return abs(50-(e-50)-r)
            
            
        def voltage(side, res, curr, distance, distance_prim, direction):

            '''
            Calculates the voltage value in a given point.

            side --> Information about the placement of the electrodes - What layer are they on? Are they on the same layer?

            res --> Information about the resistivity values of both of the layers.

            curr --> The electrical current value in the supply circut.

            distance --> Distance between emitter and reciever.

            distance_prim --> Distance between the reciever and the reflection point of emitter.

            direction --> Information about the direction of the measurement. 1 if electrode A is the reference point or -1 if electrode B is the reference point.
            '''

            if side[1] == 0:
                k12 = (res[1]-res[0])/(res[0]+res[1])
            else:
                k12 = (res[0]-res[1])/(res[0]+res[1])

            if side[0] == True:
                return direction*(curr*res[side[2]]/(2*pi*distance)+k12*curr*res[side[2]]/(2*pi*distance_prim))
            
            return (direction*curr*res[side[2]]/(2*pi*distance))*(1-k12)

        
        result, x = [], []
        if self.system in ["Układ Wennera", "Układ Schlumbergera"]:
            print('gej')
            while self.b_position <= 100:
                vam = voltage(check_side(self.a_position, self.m_position), [env_data[0], env_data[1]], env_data[2],  self.distance1, distance_prim(self.a_position, self.m_position), 1)
                vbm = voltage(check_side(self.b_position, self.m_position), [env_data[0], env_data[1]], env_data[2],  self.distance2, distance_prim(self.b_position, self.m_position), -1)

                van = voltage(check_side(self.a_position, self.n_position), [env_data[0], env_data[1]], env_data[2],  self.distance2, distance_prim(self.a_position, self.n_position), 1)
                vbn = voltage(check_side(self.b_position, self.n_position), [env_data[0], env_data[1]], env_data[2],  self.distance1, distance_prim(self.b_position, self.n_position), -1)

                V_delta = (vam+vbm)-(van+vbn)
                
                res_a = self.geometry_factor*V_delta/env_data[2]

                result.append(res_a)
                x.append(self.middle)

                self.middle += x_delta
                self.a_position += x_delta
                self.b_position += x_delta
                self.m_position += x_delta
                self.n_position += x_delta

        else:

            if dV.variant == 'Forward':
                while self.n_position <= 100:
                    vam = voltage(check_side(self.a_position, self.m_position), [env_data[0], env_data[1]], env_data[2],  self.distance1, distance_prim(self.a_position, self.m_position), 1)
                    van = voltage(check_side(self.a_position, self.n_position), [env_data[0], env_data[1]], env_data[2],  self.distance2, distance_prim(self.a_position, self.n_position), 1)

                    V_delta = vam-van

                    res_a = self.geometry_factor*V_delta/env_data[2]

                    result.append(res_a)
                    x.append(self.middle)

                    self.middle += x_delta
                    self.a_position += x_delta
                    self.m_position += x_delta
                    self.n_position += x_delta
            else:
                while self.b_position <= 100:
                    vbm = voltage(check_side(self.b_position, self.m_position), [env_data[0], env_data[1]], env_data[2],  self.distance2, distance_prim(self.b_position, self.m_position), -1)
                    vbn = voltage(check_side(self.b_position, self.n_position), [env_data[0], env_data[1]], env_data[2],  self.distance1, distance_prim(self.b_position, self.n_position), -1)

                    V_delta = vbm-vbn

                    res_a = self.geometry_factor*V_delta/env_data[2]

                    result.append(res_a)
                    x.append(self.middle)

                    self.middle += x_delta
                    self.b_position += x_delta
                    self.m_position += x_delta
                    self.n_position += x_delta

        self.x_values = x        
        return result