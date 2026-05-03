"""
Linear Search — Classical Deterministic Approach (P Class)
Problem: Search for an element in an unsorted list
Complexity: O(n) — polynomial time

This is a P-class algorithm because it solves the search problem
in polynomial time relative to the input size.
"""
import time
import random


def linear_search(arr, target):
    """
    Linear search through an unsorted array.
    Returns (index, steps) where index is the position of target
    and steps is the number of comparisons made.
    """
    steps = 0
    for i, val in enumerate(arr):
        steps += 1
        if val == target:
            return i, steps
    return -1, steps


def run_experiment(n):
    """Run linear search on an array of size n and return timing + step data."""
    arr = list(range(n))
    random.shuffle(arr)
    target = arr[n // 2]  # pick a random element

    start = time.perf_counter()
    idx, steps = linear_search(arr, target)
    elapsed = (time.perf_counter() - start) * 1e6  # microseconds

    return {
        'input_size': n,
        'index_found': idx,
        'steps': steps,
        'time_us': elapsed
    }


if __name__ == '__main__':
    print("=" * 60)
    print("  LINEAR SEARCH — P-Class Algorithm  O(n)")
    print("=" * 60)

    sizes = [4, 8, 16, 32, 64, 128, 256, 512, 1024]
    print(f"\n{'Input Size':>12} {'Steps':>8} {'Time (µs)':>12} {'Index':>8}")
    print("-" * 45)

    for n in sizes:
        result = run_experiment(n)
        print(f"{result['input_size']:>12} {result['steps']:>8} "
              f"{result['time_us']:>12.2f} {result['index_found']:>8}")

    print("\n✅ Linear Search grows linearly with input size.")
    print("   Average case: n/2 comparisons, Worst case: n comparisons.\n")