import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

# Step 1: Generate Entangled Qubits
def generate_entangled_pairs(n):
    """
    Generate a quantum circuit creating n Bell pairs (entangled qubits).
    """
    qc = QuantumCircuit(2 * n)  # 2n qubits: n pairs of entangled qubits
    for i in range(n):
        qc.h(2 * i)             # Apply Hadamard gate to the first qubit
        qc.cx(2 * i, 2 * i + 1) # Apply CNOT gate to entangle the pair
    return qc

# Step 2: Random Measurement Bases
def generate_random_bases(n):
    """
    Generate random measurement bases for Alice and Bob.
    Choices: Z-basis ('Z') or X-basis ('X').
    """
    alice_bases = np.random.choice(['Z', 'X'], n)
    bob_bases = np.random.choice(['Z', 'X'], n)
    return alice_bases, bob_bases

# Step 3: Apply Measurements
def measure_entangled_pairs(qc, alice_bases, bob_bases):
    """
    Apply measurement operators based on Alice's and Bob's chosen bases.
    """
    n = len(alice_bases)
    for i in range(n):
        if alice_bases[i] == 'X':
            qc.h(2 * i)  # Apply H gate to measure in X-basis (Alice)
        if bob_bases[i] == 'X':
            qc.h(2 * i + 1)  # Apply H gate to measure in X-basis (Bob)
    qc.measure_all()  # Measure all qubits
    return qc

# Step 4: Simulate Results
def simulate_circuit(qc):
    """
    Simulate the quantum circuit to get measurement results.
    """
    from qiskit import transpile, Aer, execute
    sim = Aer.get_backend('aer_simulator')
    qc_t = transpile(qc, sim)
    result = execute(qc_t, sim, shots=1).result()
    counts = result.get_counts()
    return list(counts.keys())[0]  # Return a single result as a string

# Step 5: Reconcile Results and Extract Key
def extract_key(measurement_results, alice_bases, bob_bases):
    """
    Compare Alice's and Bob's measurement bases and extract the shared key.
    """
    n = len(alice_bases)
    alice_key = []
    bob_key = []
    for i in range(n):
        if alice_bases[i] == bob_bases[i]:  # Only consider matching bases
            alice_key.append(int(measurement_results[2 * i]))
            bob_key.append(int(measurement_results[2 * i + 1]))
    return alice_key, bob_key

# Visualization: Plot Alice's and Bob's Results
def plot_results(alice_bases, bob_bases, alice_key, bob_key):
    indices = np.arange(len(alice_key))
    plt.bar(indices - 0.15, alice_key, width=0.3, label='Alice\'s Key', color='blue')
    plt.bar(indices + 0.15, bob_key, width=0.3, label='Bob\'s Key', color='red')
    plt.xticks(indices, [f'Bit {i}' for i in range(len(alice_key))])
    plt.title("Shared Key Between Alice and Bob")
    plt.ylabel("Bit Value")
    plt.legend()
    plt.show()

# Main Function
if __name__ == "__main__":
    n = 5  # Number of entangled pairs
    print("\n--- E91 Quantum Key Distribution Protocol ---")

    # Step 1: Generate Entangled Pairs
    print("Step 1: Generating entangled qubit pairs...")
    entanglement_circuit = generate_entangled_pairs(n)
    print("Generated entanglement circuit:")
    entanglement_circuit.draw('mpl')
    plt.show()

    # Step 2: Choose Random Bases
    print("\nStep 2: Generating random measurement bases...")
    alice_bases, bob_bases = generate_random_bases(n)
    print("Alice's bases:", alice_bases)
    print("Bob's bases:  ", bob_bases)

    # Step 3: Apply Measurements
    print("\nStep 3: Applying measurements based on chosen bases...")
    qc = measure_entangled_pairs(entanglement_circuit, alice_bases, bob_bases)
    print("Quantum circuit with measurements:")
    qc.draw('mpl')
    plt.show()

    # Step 4: Simulate Results
    print("\nStep 4: Simulating the circuit to get measurement results...")
    measurement_results = simulate_circuit(qc)
    print("Measurement results:", measurement_results)

    # Step 5: Reconcile Results and Extract Key
    print("\nStep 5: Reconciling bases and extracting the shared key...")
    alice_key, bob_key = extract_key(measurement_results, alice_bases, bob_bases)
    print("Alice's key:", alice_key)
    print("Bob's key:  ", bob_key)

    # Visualization
    print("\nStep 6: Visualizing the shared key...")
    plot_results(alice_bases, bob_bases, alice_key, bob_key)
