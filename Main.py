import functions as f
from math import pi

resistance_1 = f.check(f.check_float(input('Set the electrical resistance of the first layer [Ωm]: ')), [0, 1000000], 'range')
resistance_2 = f.check(f.check_float(input('\nSet the electrical resistance of the second layer [Ωm]: ')), [0, 1000000], 'range')

current = f.check(f.check_float(input('\nSet the current value in the supply circut [A]: ')), [0, 1000000], 'range')

mes_system = f.check(input('\nWhat measuring system do you want to use?\n1 -> Wenner\'s System\n2 -> Schlumberger\'s System\n3 -> Three-electrode System\nSelect: '), ['1', '2', '3'], 'choice')
if mes_system == '3':
    variant = f.check(input('\nWhat profiling variant do you want to use?\n1 -> Forward\n2 -> Backward\nSelect: '), ['1', '2'], 'choice')

ambn = f.check(f.check_float(input('\nSet the distance between A-M and B-N electrodes: ')), [0, 10], 'range')
mn = f.check(f.check_float(input('\nSet the distance between M-N electrodes: ')), [0, 10], 'range')
geometry_factor = pi*ambn*(ambn+mn)/mn
print(geometry_factor)