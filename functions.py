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