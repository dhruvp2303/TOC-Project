"""
Brute Force / Exhaustive Search — NP-Style Approach
Problem: Search for an element in an unsorted list
Complexity: O(n²) — simulating non-deterministic exhaustive checking

This simulates an NP-style brute-force approach where we redundantly
check all possibilities (nested loop), representing the worst-case
behavior of trying every combination before finding the answer.
"""
import time


def brute_force_search(arr, target):
    """
    Exhaustive brute-force search with nested loops.
    Simulates NP-style checking of all possibilities.
    Returns (index, steps) where steps counts total comparisons.
    """
    steps = 0
    for i in range(len(arr)):
        for j in range(len(arr)):
            steps += 1
            if arr[j] == target:
                return j, steps
    return -1, steps


def run_experiment(n):
    """Run brute force search on an array of size n and return timing + step data."""
    arr = list(range(n))
    target = n // 2  # pick middle element

    start = time.perf_counter()
    idx, steps = brute_force_search(arr, target)
    elapsed = (time.perf_counter() - start) * 1e6  # microseconds

    return {
        'input_size': n,
        'index_found': idx,
        'steps': steps,
        'time_us': elapsed
    }


if __name__ == '__main__':
    print("=" * 60)
    print("  BRUTE FORCE SEARCH — NP-Style Algorithm  O(n²)")
    print("=" * 60)

    sizes = [4, 8, 16, 32, 64, 128, 256]
    print(f"\n{'Input Size':>12} {'Steps':>10} {'Time (µs)':>14} {'Index':>8}")
    print("-" * 50)

    for n in sizes:
        result = run_experiment(n)
        print(f"{result['input_size']:>12} {result['steps']:>10} "
              f"{result['time_us']:>14.2f} {result['index_found']:>8}")

    print("\n⚠️  Brute Force grows quadratically (n²) with input size.")
    print("   Much slower than linear search for large inputs.\n")