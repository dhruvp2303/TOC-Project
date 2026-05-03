import matplotlib.pyplot as plt
import numpy as np

sizes = [4, 8, 16, 64, 256]
classical = [2, 4, 8, 32, 128]
brute = [8, 32, 128, 2048, 32768]
quantum = [1, 2, 3, 6, 13]

plt.figure(figsize=(10, 5))
plt.plot(sizes, classical, 'o-', label='Classical O(n)', color='green')
plt.plot(sizes, brute, 's--', label='NP Brute Force O(n²)', color='orange')
plt.plot(sizes, quantum, '^-', label="Quantum Grover O(√n)", color='purple')
plt.xlabel('Input Size (n)')
plt.ylabel('Steps / Iterations')
plt.title('P vs NP vs Quantum — Unsorted Search Performance')
plt.legend()
plt.yscale('log')
plt.grid(True, alpha=0.3)
plt.savefig('comparison_chart.png', dpi=150)
plt.show()
