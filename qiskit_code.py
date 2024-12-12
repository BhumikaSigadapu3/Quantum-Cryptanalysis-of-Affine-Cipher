!pip install qiskit-aer
from qiskit import QuantumCircuit, transpile, assemble
from qiskit.circuit.library import QFT, MCXGate
from qiskit.visualization import plot_histogram
from qiskit_aer import Aer
#Implementation of Q-Q Adder
def modular_adder(n):
    qc = QuantumCircuit(n + 1)
    for i in range(n):
        qc.cx(i, n)
    qc.barrier()
    return qc
#Implementation of Q-Q Binary Multiplier
def modular_multiplier(n):
    qc = QuantumCircuit(2 * n + 1)
    for i in range(n):
        qc.cx(i, n + i)
    qc.barrier()
    qc.barrier()
    return qc
#Setting up grover's diffuser
def grover_diffuser(n):
    qc = QuantumCircuit(n)
    qc.h(range(n))
    qc.x(range(n))
    qc.h(n - 1)
    qc.append(MCXGate(n - 1), list(range(n)))
    qc.h(n - 1)
    qc.x(range(n))
    qc.h(range(n))
    return qc

#Initialising the plain text
n = 3
qc = QuantumCircuit(2 * n + 1, n)
qc.x(0)
qc.x(1)
qc.x(2)

#The qubit is 111 we need to get this as highest number of times in output
qc.barrier()

qc.append(modular_adder(n), range(n + 1))
qc.barrier()

qc.append(modular_multiplier(n), range(2 * n + 1))
qc.barrier()

qc.append(grover_diffuser(n), range(n))
qc.barrier()

qc.measure(range(n), range(n))

sim = Aer.get_backend('qasm_simulator')
transpiled_qc = transpile(qc, sim)
job = sim.run(transpiled_qc, shots=1024)
results = job.result()
counts = results.get_counts()

print(counts)
plot_histogram(counts)
