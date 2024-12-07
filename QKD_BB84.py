import numpy as np
from qiskit import QuantumCircuit
from qiskit.visualization import plot_bloch_multivector
from qiskit.quantum_info import Statevector
import matplotlib.pyplot as plt

# Step 1: Generate random bits and bases
def generate_random_bits_and_bases(n):
    """
    Generate random bits (0 or 1) and random bases (+ or x).
    """
    bits = np.random.randint(0, 2, n)
    bases = np.random.choice(['+', 'x'], n)
    return bits, bases

# Step 2: Encode qubits using quantum methods
def encode_qubits_quantum(bits, bases):
    """
    Encode qubits based on bits and bases using a quantum circuit.
    """
    n = len(bits)
    qc = QuantumCircuit(n)
    for i in range(n):
        if bits[i] == 1:
            qc.x(i)  # Apply X gate for bit 1
        if bases[i] == 'x':
            qc.h(i)  # Apply H gate for diagonal basis
    return qc

# Step 3: Simulate measurements with quantum Statevector
def measure_qubits_quantum(qc, bob_bases):
    """
    Simulate measurement results using quantum statevector.
    """
    n = len(bob_bases)
    for i in range(n):
        if bob_bases[i] == 'x':
            qc.h(i)  # Apply H gate to measure in the diagonal basis
    # Get the statevector and visualize it
    state = Statevector.from_instruction(qc)
    print("\nQuantum State Visualization (Bloch Sphere):")
    plot_bloch_multivector(state).show()
    
    # Simulate a single-shot measurement (pick random outcome)
    probabilities = state.probabilities_dict()
    result = np.random.choice(list(probabilities.keys()), p=list(probabilities.values()))
    return result

# Step 4: Classical BB84 simulation
def classical_bb84_simulation(alice_bits, alice_bases, bob_bases):
    """
    Simulate BB84 classically without quantum mechanics.
    """
    n = len(alice_bits)
    results = []
    for i in range(n):
        if alice_bases[i] == bob_bases[i]:
            results.append(alice_bits[i])  # Correct if bases match
        else:
            results.append(np.random.randint(0, 2))  # Random guess
    return results

# Step 5: Reconcile bases
def reconcile_bases(alice_bases, bob_bases, results):
    """
    Reconcile Alice's and Bob's bases to generate the shared key.
    """
    key = [results[i] for i in range(len(alice_bases)) if alice_bases[i] == bob_bases[i]]
    return key

# Visualization: Plot Alice's and Bob's data
def plot_bb84_results(alice_bits, alice_bases, bob_bases, bob_results):
    n = len(alice_bits)
    indices = np.arange(n)
    
    fig, ax = plt.subplots(2, 1, figsize=(10, 6))
    
    # Alice's bits and bases
    ax[0].bar(indices, alice_bits, color='blue', label='Alice\'s Bits')
    ax[0].set_xticks(indices)
    ax[0].set_title("Alice's Bits and Bases")
    ax[0].legend()
    for i in range(n):
        ax[0].text(i, alice_bits[i] + 0.1, f"{alice_bases[i]}", ha='center', fontsize=10)
    
    # Bob's results and bases
    ax[1].bar(indices, bob_results, color='red', label='Bob\'s Results')
    ax[1].set_xticks(indices)
    ax[1].set_title("Bob's Results and Bases")
    ax[1].legend()
    for i in range(n):
        ax[1].text(i, bob_results[i] + 0.1, f"{bob_bases[i]}", ha='center', fontsize=10)
    
    plt.tight_layout()
    plt.show()

# Main Function
if __name__ == "__main__":
    n = 10  # Number of bits/qubits
    mode = input("Choose mode ('quantum' or 'classical'): ").strip().lower()

    # Alice's steps
    alice_bits, alice_bases = generate_random_bits_and_bases(n)
    print("\nAlice's bits:", alice_bits)
    print("Alice's bases:", alice_bases)

    # Bob's steps
    bob_bases = np.random.choice(['+', 'x'], n)
    print("Bob's bases:", bob_bases)

    if mode == "quantum":
        print("\n--- Running Quantum Simulation ---")
        # Quantum Encoding
        qc = encode_qubits_quantum(alice_bits, alice_bases)
        print("Alice's Quantum Circuit:")
        qc.draw('mpl')  # Visualize circuit using matplotlib
        plt.show()      # Ensure the plot is displayed

        
        # Quantum Measurement
        bob_results_str = measure_qubits_quantum(qc, bob_bases)
        bob_results = [int(bob_results_str[-(i+1)]) for i in range(n)]  # Extract bit results
    elif mode == "classical":
        print("\n--- Running Classical Simulation ---")
        bob_results = classical_bb84_simulation(alice_bits, alice_bases, bob_bases)
    else:
        print("Invalid mode. Please choose 'quantum' or 'classical'.")
        exit()

    print("Bob's measurement results:", bob_results)

    # Reconcile bases and generate shared key
    shared_key = reconcile_bases(alice_bases, bob_bases, bob_results)
    print("Shared key:", shared_key)

    # Visualization
    print("\n--- Visualizing Results ---")
    plot_bb84_results(alice_bits, alice_bases, bob_bases, bob_results)
