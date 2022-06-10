# import pennylane as qml


# dev = qml.device('forest.qpu', wires =2)

# @qml.qnode(dev)
# def my_quantum_function():
#     qml.Hadamard(wires=[0])
#     qml.CNOT(wires = [0,1])
#     return qml.expval(qml.PauliZ(0)@qml.PauliZ(1))

# print(my_quantum_function())

import pennylane as qml
from pennylane_qiskit import AerDevice

# dev = AerDevice(wires=2)
dev = qml.device('default.qubit', wires=2, shots=None)


@qml.qnode(dev)
def my_quantum_function():
    qml.Hadamard(wires=[0])
    qml.CNOT(wires=[0,1])
    return qml.state()

circuit = qml.QNode(my_quantum_function, dev)
drawer = qml.draw(circuit)
print(drawer())

print(circuit())