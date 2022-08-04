from qiskit import QuantumCircuit, assemble, Aer
from qiskit.visualization import plot_histogram, plot_bloch_vector
from math import sqrt, pi
from qiskit.quantum_info import Statevector
import numpy as np
import matplotlib.pyplot as plt
import random
num = 5
num_round = 5
# Create a quantum circuit acting on a quantum register of 20 qubits
circ=QuantumCircuit(num)
sim = Aer.get_backend('aer_simulator') 
# some initial_state can be 1
initial_state = [0,1]
g = 0.97

# Get a random number for qubit that start as 1
number_of_qubit_1 = np.random.randint(0,num,size=1)
array_qubit1_pos = np.random.randint(0,num,size = number_of_qubit_1)
# Get a random position for # of qubit that start as 1
array_qubit1_pos = list(dict.fromkeys(array_qubit1_pos))

# Generate ranodm initial state
for bit in array_qubit1_pos:
    circ.initialize(initial_state, bit)

# Number of period 
for j in range(num_round):

# apply rotation by pi g
    for i in range(num):
        circ.rx(pi*g, i)


# add ising interaction gate
    for i in range(num-1):
        random_j = np.random.uniform(-1.5*np.pi, -0.5*np.pi)
        circ.rzz(random_j,i,i+1)


#add random field gate:
    for i in range(num):
        random_field = np.random.uniform(-np.pi,np.pi)
        circ.rz(random_field, i)
circ.save_statevector()




# I should find a way to measure the expectation value of qubit x
qobj = assemble(circ)     # Create a Qobj from the circuit for the simulator to run
result = sim.run(qobj).result() 
out_state = result.get_statevector()
print(f"here {circ.measure_all()}")
circ.draw()
print(out_state)
qobj = assemble(circ)
result = sim.run(qobj).result()
counts = result.get_counts()
plot_histogram(counts)
circ.draw('mpl')
plt.show()