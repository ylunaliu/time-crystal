from qiskit import QuantumCircuit, assemble, Aer
from qiskit.visualization import plot_histogram, plot_bloch_vector
from math import sqrt, pi
from qiskit.quantum_info import Statevector
import numpy as np
import matplotlib.pyplot as plt
import random


def create_quantum_circuit(num_round, g, num_bits, array_pos_qubit1, random_j, random_field):
    """
    Create quantum circuit for number of period with saved parameter
    initial_state: array with 
    """
    one_state = [0,1]
    sim = Aer.get_backend('aer_simulator') 
    circ=QuantumCircuit(num_bits)
    for bit in array_pos_qubit1:
        circ.initialize(one_state, bit)
    circ.barrier()

    for j in range(num_round):
        for i in range(num_bits):
            circ.rx(pi*g, i)
        circ.barrier()

        for i in range(num_bits-1):
            circ.rzz(random_j[i], i, i+1)
        circ.barrier()

        for i in range(num_bits):
            circ.rz(random_field[i],i)
        circ.barrier()
    circ.save_statevector()

    qobj = assemble(circ)
    result = sim.run(qobj).result() 
    out_state = result.get_statevector()
    circ.measure_all()
    qobj = assemble(circ)
    result = sim.run(qobj).result() 
    counts = result.get_counts()
    # print(f"counts: {counts}")
    return(counts)