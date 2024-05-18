from math import pi

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




class measurement:

    def __init__(self):
        None

    def set_geometry(self, system):
        
        if system == '1':
            self.ambn = check(check_float(input('\nSet the distance between electrodes [m]: ')), [0, 10], 'range')
            self.mn = self.ambn
            self.a_position = 0
            self.b_position = 3*self.ambn
            self.m_position = self.ambn
            self.n_position = 2*self.ambn
            self.middle = self.ambn+self.ambn/2
            self.geometry_factor = pi*2*self.ambn

        elif system == '2':
            self.ambn = check(check_float(input('\nSet the distance between A-M and B-N electrodes [m]: ')), [0, 10], 'range')
            self.mn = check(check_float(input('\nSet the distance between M-N electrodes [m]: ')), [0, 10], 'range')
            self.a_position = 0
            self.b_position = 2*self.ambn+self.mn
            self.m_position = self.ambn
            self.n_position = self.ambn+self.mn
            self.middle = self.ambn+self.mn/2
            self.geometry_factor = pi*self.ambn*(self.ambn+self.mn)/self.mn

        else:
            self.variant = check(input('\nWhat profiling variant do you want to use?\n1 -> Forward\n2 -> Backward\nSelect: '), ['1', '2'], 'choice')
            self.ambn = check(check_float(input('\nSet the distance between A-M electrodes [m]: ')), [0, 10], 'range')
            self.mn = check(check_float(input('\nSet the distance between M-N electrodes [m]: ')), [0, 10], 'range')
            
            if self.variant == '1':
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

            self.geometry_factor = pi*self.ambn*(self.ambn+self.mn)/self.mn
            
    def measure(self, system, x_delta, env_data):

        def check_side(p1,p2):
            if (p1 < 50 and p2 <= 50):
                return [True, 0, 0]
            elif (p1 >= 50 and p2 > 50):
                return [True, 1, 1]
            elif (p1 < 50 and p2 > 50):
                return [False, 0, 1]
            else:
                return [False, 1, 0]
            
        def distance_prim(p1,p2):
            if p1 <=50:
                return abs(50+(50-p1)-p2)
            else:
                return abs(50-(p1-50)-p2)
            
            
        def voltage(side, res, curr, distance, distance_prim):

            if side[1] == 0:
                k12 = (res[1]-res[0])/(res[0]+res[1])
            else:
                k12 = (res[0]-res[1])/(res[0]+res[1])

            if side[0] == True:
                v = curr*res[side[2]]/(2*pi*distance)+k12*curr*res[side[2]]/(2*pi*distance_prim)
            else:
                v = curr*res[side[2]]/(2*pi*distance)*(1-k12)
            return v
        
        result = []
        x = []
        if system in ['1', '2']:
            if system == '1':
                distance1 = self.ambn
                distance2 = 2*self.ambn
            else:
                distance1 = self.ambn
                distance2 = self.ambn+self.mn
            while self.b_position <= 100:
                vam = voltage(check_side(self.a_position, self.m_position), [env_data[0], env_data[1]], env_data[2],  distance1, distance_prim(self.a_position, self.m_position))
                vbm = voltage(check_side(self.b_position, self.m_position), [env_data[0], env_data[1]], env_data[2],  distance2, distance_prim(self.b_position, self.m_position))

                van = voltage(check_side(self.a_position, self.n_position), [env_data[0], env_data[1]], env_data[2],  distance2, distance_prim(self.a_position, self.n_position))
                vbn = voltage(check_side(self.b_position, self.n_position), [env_data[0], env_data[1]], env_data[2],  distance1, distance_prim(self.b_position, self.n_position))


                V_delta = (vam+vbm)-(van+vbn)
                

                res_a = self.geometry_factor*V_delta/env_data[2]
                result.append(res_a)

                x.append(self.middle)
                self.middle += x_delta
                self.a_position += x_delta
                self.b_position += x_delta
                self.m_position += x_delta
                self.n_position += x_delta
        self.x_values = x        
        return result