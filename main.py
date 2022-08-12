from qiskit import IBMQ, transpile
from qiskit.providers.ibmq.managed import IBMQJobManager
from qiskit.circuit.random import random_circuit
from qiskit.quantum_info import Statevector
import numpy as np
import matplotlib.pyplot as plt
from create_circuits import create_quantum_circuit
from create_circuits import initial_state
from create_circuits import echo_circuit
from qiskit import IBMQ
# IBMQ.save_account('878d1c322b1955198a0d63ea1f7f352b50f5356cd6a8ac873681044dc92044f5d70262025c24ec676fcb318fa4db813fdab86516c643ee1f2070695b88a9815e')
provider = IBMQ.load_account()
backend = provider.backend.ibmq_manila
# backend = provider.get_backend('ibmq_qasm_simulator')
num_bits = 5
num_round = 30
g = 0.97
g2 = 0.6
qubit_to_measure = 3
save_parameter = []
# fname = "saved_p.txt"
# Get random initial state
number_of_qubit_1 = np.random.randint(0,num_bits,size=1)
array_qubit1_pos = list(dict.fromkeys(np.random.randint(0,num_bits,size = number_of_qubit_1)))
save_parameter.append(array_qubit1_pos)
# Get random interaction for random interaction
random_j = np.random.uniform(-1.5*np.pi, -0.5*np.pi, size = num_bits-1)
save_parameter.append(random_j)
# Get random field parameter
random_field = np.random.uniform(-np.pi,np.pi, size = num_bits)
save_parameter.append(random_field)
circs = []
print(save_parameter)
np.save("save_parameter",np.array(save_parameter))
for i in range(num_round):
    if(i==0):
        circuit = initial_state(num_bits, array_qubit1_pos)
        circs.append(circuit)
    else:
        circuit = create_quantum_circuit(i, g, num_bits, array_qubit1_pos, random_j, random_field)
        circs.append(circuit)

for i in range(num_round):
    if(i==0):
        circuit = initial_state(num_bits, array_qubit1_pos)
        circs.append(circuit)
    else:
        circuit = create_quantum_circuit(i, g2, num_bits, array_qubit1_pos, random_j, random_field)
        circs.append(circuit)

for i in range(num_round):
    if(i==0):
        circuit = initial_state(num_bits, array_qubit1_pos)
        circs.append(circuit)
    else:
        circuit = echo_circuit(i, g, num_bits, array_qubit1_pos, random_j, random_field)
        circs.append(circuit)


circs = transpile(circs, backend=backend)
job_manager = IBMQJobManager()
job_set_foo = job_manager.run(circs, backend=backend, name='foo')
results = job_set_foo.results()
data = []
for i in range(len(circs)):
    counts = results.get_counts(i)
    keys = list(counts)
    expectation_value_z_qubit = []
    COUNTER = 0
    for key in keys:
        bit_status = int(key[qubit_to_measure-1])
        # print(bit_status)
        if(bit_status==0):
            expectation_value_z = 1*int(counts[key])
            COUNTER += int(counts[key])
            # print(f"here is the counts key {counts[key]} with keys{key}")
            # print(f"here is the expectation_value when bit=0{expectation_value_z}")
            expectation_value_z_qubit.append(expectation_value_z)
        if(bit_status==1):
            expectation_value_z = -1*int(counts[key])
            COUNTER += int(counts[key])
            # print(f"here is the expectation_value when bit=1{expectation_value_z}")
            expectation_value_z_qubit.append(expectation_value_z)
    # print(len(keys))
    data.append(sum(expectation_value_z_qubit)/(COUNTER))

x = np.arange(0,num_round)
x2 = np.arange(0, num_round, 2)
print(len(x))
data_097 = data[:num_round]
print(len(data_097))
data_060 = data[num_round:num_round*2]
print(len(data_060))
echo = data[num_round*2:int(num_round*2+num_round/2)]
print(len(echo))
np.save("threethings",np.array(data))
# print(data_060)
# plt.title("g = {}".format(g) )
plt.xlabel("t")
plt.ylabel("qubit {} <Z>".format(qubit_to_measure))
plt.plot(x, data_097, '-bo')
plt.plot(x, data_060, '-go')
plt.plot(x2, echo, 'ro')
plt.savefig("data_qc.png", dpi='figure')
plt.show()

    