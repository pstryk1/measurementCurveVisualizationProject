import functions as f
from math import pi

resistance_1 = f.check(f.check_float(input('Set the electrical resistance of the first layer [Ωm]: ')), [0, 1000], 'range')
resistance_2 = f.check(f.check_float(input('\nSet the electrical resistance of the second layer [Ωm]: ')), [0, 1000], 'range')

current = f.check(f.check_float(input('\nSet the value of elctrical current in the supply circut [A]: ')), [0, 1000], 'range')

mes_system = f.check(input('\nWhat measuring system do you want to use?\n1 -> Wenner\'s System\n2 -> Schlumberger\'s System\n3 -> Three-electrode System\nSelect: '), ['1', '2', '3'], 'choice')

geometry = f.geometry()
geometry.set_geometry(mes_system)

print(geometry.a_position)
print(geometry.b_position)
print(geometry.middle)
print(geometry.geometry_factor)
print(geometry.ambn)
print(geometry.mn)

x_delta = f.check(f.check_float(input('\nSet the distance between every measurement point: ')), [0, 10], 'range')

