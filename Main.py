import functions as f
from math import pi
from matplotlib import pyplot as plt

resistance_1 = f.check(f.check_float(input('Set the electrical resistance of the first layer [Ωm]: ')), [0, 1000], 'range')
resistance_2 = f.check(f.check_float(input('\nSet the electrical resistance of the second layer [Ωm]: ')), [0, 1000], 'range')
current = f.check(f.check_float(input('\nSet the value of elctrical current in the supply circut [A]: ')), [0, 1000], 'range')
#k12 = (resistance_2-resistance_1)/(resistance_1+resistance_2)
env_data = [resistance_1, resistance_2, current]

mes_system = f.check(input('\nWhat measuring system do you want to use?\n1 -> Wenner\'s System\n2 -> Schlumberger\'s System\n3 -> Three-electrode System\nSelect: '), ['1', '2', '3'], 'choice')

measurement = f.measurement(mes_system)

#print(measurement.a_position)
#print(measurement.b_position)
#print(measurement.middle)
print(measurement.geometry_factor)
#print(measurement.ambn)
#print(measurement.mn)

x_delta = f.check(f.check_float(input('\nSet the distance between every measurement point: ')), [0, 10], 'range')


y = measurement.measure(mes_system, x_delta, env_data)
print(y)

figure = plt.figure()
ax = figure.add_subplot()
ax.set_xticks([i for i in range(0,100) if i%2 == 0])
plt.plot(measurement.x_values, y)
#plt.scatter(measurement.x_values, y)
#plt.yscale('log')
plt.grid()
plt.show()