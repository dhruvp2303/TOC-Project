"""
Performance Comparison Chart — P vs NP vs Quantum
Generates a visual comparison of algorithmic complexity growth.
"""
import matplotlib.pyplot as plt
import numpy as np

sizes = [4, 8, 16, 32, 64, 128, 256]
classical = [s // 2 for s in sizes]          # O(n) avg
brute = [(s * (s//2 + 1)) for s in sizes]    # O(n²)
quantum = [int(np.floor(np.pi/4 * np.sqrt(s))) for s in sizes]  # O(√n)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Chart 1: Steps (Log Scale)
ax1.plot(sizes, classical, 'o-', label='P: Linear Search O(n)', color='#22c55e', lw=2)
ax1.plot(sizes, brute, 's--', label='NP: Brute Force O(n²)', color='#f97316', lw=2)
ax1.plot(sizes, quantum, '^-', label="Quantum: Grover O(√n)", color='#a855f7', lw=2)
ax1.set_xlabel('Input Size (n)')
ax1.set_ylabel('Steps / Iterations')
ax1.set_title('P vs NP vs Quantum — Steps (Log Scale)')
ax1.legend()
ax1.set_yscale('log')
ax1.grid(True, alpha=0.3)

# Chart 2: Linear Scale
ax2.plot(sizes, classical, 'o-', label='P: Linear O(n)', color='#22c55e', lw=2)
ax2.plot(sizes, brute, 's--', label='NP: Brute Force O(n²)', color='#f97316', lw=2)
ax2.plot(sizes, quantum, '^-', label="Quantum: Grover O(√n)", color='#a855f7', lw=2)
ax2.set_xlabel('Input Size (n)')
ax2.set_ylabel('Steps / Iterations')
ax2.set_title('P vs NP vs Quantum — Steps (Linear Scale)')
ax2.legend()
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('comparison_chart.png', dpi=150, bbox_inches='tight')
plt.show()
print("Chart saved as comparison_chart.png")
