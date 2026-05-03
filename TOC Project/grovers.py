"""
Grover's Algorithm — Quantum Computing Approach
Problem: Search for an element in an unsorted database
Complexity: O(√n) — quadratic speedup over classical

Uses Qiskit with the AerSimulator for local quantum simulation.
Grover's algorithm provides a provable quadratic speedup over
classical search, finding an element in O(√N) queries instead of O(N).
"""
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
import numpy as np
import time


def grovers_search(n_qubits, target_index):
    """
    Grover's Algorithm for unsorted search.

    Parameters:
        n_qubits: number of qubits (database size = 2^n_qubits)
        target_index: the index we're searching for

    Returns:
        found_index, iterations, elapsed_ms, counts
    """
    N = 2 ** n_qubits
    iterations = int(np.floor(np.pi / 4 * np.sqrt(N)))

    qc = QuantumCircuit(n_qubits, n_qubits)

    # Step 1: Apply Hadamard to all qubits (equal superposition)
    qc.h(range(n_qubits))

    for _ in range(iterations):
        # Step 2: Oracle — flip the phase of the target state
        target_bin = format(target_index, f'0{n_qubits}b')
        for i, bit in enumerate(reversed(target_bin)):
            if bit == '0':
                qc.x(i)
        qc.h(n_qubits - 1)
        qc.mcx(list(range(n_qubits - 1)), n_qubits - 1)
        qc.h(n_qubits - 1)
        for i, bit in enumerate(reversed(target_bin)):
            if bit == '0':
                qc.x(i)

        # Step 3: Diffusion operator (amplitude amplification)
        qc.h(range(n_qubits))
        qc.x(range(n_qubits))
        qc.h(n_qubits - 1)
        qc.mcx(list(range(n_qubits - 1)), n_qubits - 1)
        qc.h(n_qubits - 1)
        qc.x(range(n_qubits))
        qc.h(range(n_qubits))

    # Measure all qubits
    qc.measure(range(n_qubits), range(n_qubits))

    # Run on Aer Simulator
    sim = AerSimulator()
    start = time.perf_counter()
    result = sim.run(qc, shots=1024).result()
    elapsed = (time.perf_counter() - start) * 1e3  # milliseconds

    counts = result.get_counts()
    most_likely = max(counts, key=counts.get)
    found_index = int(most_likely, 2)

    return found_index, iterations, elapsed, counts


def run_experiment(n_qubits, target_index):
    """Run Grover's search and return structured results."""
    found, iters, elapsed_ms, counts = grovers_search(n_qubits, target_index)
    N = 2 ** n_qubits
    return {
        'n_qubits': n_qubits,
        'database_size': N,
        'target': target_index,
        'found': found,
        'correct': found == target_index,
        'iterations': iters,
        'time_ms': elapsed_ms,
        'counts': counts
    }


if __name__ == '__main__':
    print("=" * 60)
    print("  GROVER'S ALGORITHM — Quantum Search  O(√n)")
    print("=" * 60)

    experiments = [
        (2, 2),   # 4-element database, search for index 2
        (3, 5),   # 8-element database, search for index 5
        (4, 11),  # 16-element database, search for index 11
        (5, 21),  # 32-element database, search for index 21
    ]

    print(f"\n{'Qubits':>8} {'DB Size':>10} {'Target':>8} {'Found':>8} "
          f"{'Correct':>9} {'Iterations':>12} {'Time (ms)':>12}")
    print("-" * 75)

    for n_q, tgt in experiments:
        r = run_experiment(n_q, tgt)
        print(f"{r['n_qubits']:>8} {r['database_size']:>10} {r['target']:>8} "
              f"{r['found']:>8} {'✅' if r['correct'] else '❌':>9} "
              f"{r['iterations']:>12} {r['time_ms']:>12.2f}")

    print("\n🔬 Grover's Algorithm grows as O(√n) — quadratic speedup!")
    print("   Uses quantum superposition and amplitude amplification.\n")

    # Show measurement distribution for 3-qubit case
    print("Measurement Distribution (3-qubit, target=5):")
    r = run_experiment(3, 5)
    for state, count in sorted(r['counts'].items()):
        bar = '█' * (count // 10)
        marker = " ← TARGET" if int(state, 2) == 5 else ""
        print(f"  |{state}⟩ = {count:>4}  {bar}{marker}")
