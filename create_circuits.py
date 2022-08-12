from qiskit import QuantumCircuit, assemble, Aer
from qiskit.visualization import plot_histogram, plot_bloch_vector
from math import sqrt, pi
from qiskit.quantum_info import Statevector
import numpy as np
import matplotlib.pyplot as plt
import random

def initial_state(num_bits, array_pos_qubit1):
    one_state = [0,1]
    circ=QuantumCircuit(num_bits)
    for bit in array_pos_qubit1:
        circ.initialize(one_state, bit)
    circ.barrier()
    circ.measure_all()
    return circ

def echo_circuit(num_round, g, num_bits, array_pos_qubit1, random_j, random_field):
    one_state = [0,1]
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

    for j in reversed(range(num_round)):
        for i in range(num_bits):
            circ.rz(-random_field[i],i)
        circ.barrier()

        for i in range(num_bits-1):
            circ.rzz(-random_j[i], i, i+1)
        circ.barrier()

        for i in range(num_bits):
            circ.rx(-pi*g, i)
        circ.barrier()

    # for bit in range(num_bits):
    #     if(bit not in array_pos_qubit1):
    #         circ.initialize(one_state, bit)
    # circ.barrier()
       
    circ.measure_all()
    return circ

def create_quantum_circuit(num_round, g, num_bits, array_pos_qubit1, random_j, random_field):
    """
    Create quantum circuit for number of period with saved parameter
    initial_state: array with 
    """
    one_state = [0,1]
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
    circ.measure_all()
    # circ.save_statevector()
    return circ
    # qobj = assemble(circ)
    # result = sim.run(qobj).result() 
    # out_state = result.get_statevector()
    
    # qobj = assemble(circ)
    # result = sim.run(qobj).result() 
    # counts = result.get_counts()
    # # print(f"counts: {counts}")
    # return(counts)