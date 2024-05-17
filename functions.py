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

class geometry:

    def __init__(self):
        None

    def set_geometry(self, system):
        
        if system == '1':
            self.ambn = check(check_float(input('\nSet the distance between electrodes [m]: ')), [0, 10], 'range')
            self.mn = None
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
            

    