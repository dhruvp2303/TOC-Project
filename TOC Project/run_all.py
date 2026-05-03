"""
Experimental Study of P, NP and Quantum Computing using Simulation Tools
=========================================================================
Problem: Search in Unsorted List
- Classical P: Linear Search O(n)
- NP Brute Force: Exhaustive Search O(n²)  
- Quantum: Grover's Algorithm O(√n)

Generates a comprehensive HTML report with:
- Individual algorithm results
- Multi-size experimentation table (Step 4)
- Performance comparison charts
- Grover's measurement distribution
- Analysis section (Step 6)
- Conclusion (Step 7)
"""
import time, random, json, os, base64, math

# ═══════════════════════════════════════════════════
# 1. ALGORITHM DEFINITIONS
# ═══════════════════════════════════════════════════

def linear_search(arr, target):
    steps = 0
    for i, val in enumerate(arr):
        steps += 1
        if val == target:
            return i, steps
    return -1, steps

def brute_force_search(arr, target):
    steps = 0
    for i in range(len(arr)):
        for j in range(len(arr)):
            steps += 1
            if arr[j] == target:
                return j, steps
    return -1, steps

# ═══════════════════════════════════════════════════
# 2. MULTI-SIZE EXPERIMENTATION (Step 4)
# ═══════════════════════════════════════════════════

exp_sizes = [4, 8, 16, 32, 64, 128, 256]
experiments = []

for n in exp_sizes:
    arr = list(range(n))
    random.shuffle(arr)
    target = arr[n // 2]

    # Linear Search
    start = time.perf_counter()
    ls_idx, ls_steps = linear_search(arr, target)
    ls_time = (time.perf_counter() - start) * 1e6

    # Brute Force
    bf_arr = list(range(n))
    bf_target = n // 2
    start = time.perf_counter()
    bf_idx, bf_steps = brute_force_search(bf_arr, bf_target)
    bf_time = (time.perf_counter() - start) * 1e6

    # Quantum (theoretical steps)
    q_iters = int(math.floor(math.pi / 4 * math.sqrt(n)))

    experiments.append({
        'n': n, 'ls_steps': ls_steps, 'ls_time': ls_time,
        'bf_steps': bf_steps, 'bf_time': bf_time, 'q_iters': q_iters
    })

# ═══════════════════════════════════════════════════
# 3. GROVER'S ALGORITHM (Quantum Simulation)
# ═══════════════════════════════════════════════════

try:
    from qiskit import QuantumCircuit
    from qiskit_aer import AerSimulator
    import numpy as np

    def grovers_search(n_qubits, target_index):
        N = 2 ** n_qubits
        iterations = int(np.floor(np.pi / 4 * np.sqrt(N)))
        qc = QuantumCircuit(n_qubits, n_qubits)
        qc.h(range(n_qubits))
        for _ in range(iterations):
            target_bin = format(target_index, f'0{n_qubits}b')
            for i, bit in enumerate(reversed(target_bin)):
                if bit == '0': qc.x(i)
            qc.h(n_qubits - 1)
            qc.mcx(list(range(n_qubits - 1)), n_qubits - 1)
            qc.h(n_qubits - 1)
            for i, bit in enumerate(reversed(target_bin)):
                if bit == '0': qc.x(i)
            qc.h(range(n_qubits))
            qc.x(range(n_qubits))
            qc.h(n_qubits - 1)
            qc.mcx(list(range(n_qubits - 1)), n_qubits - 1)
            qc.h(n_qubits - 1)
            qc.x(range(n_qubits))
            qc.h(range(n_qubits))
        qc.measure(range(n_qubits), range(n_qubits))
        sim = AerSimulator()
        start = time.perf_counter()
        result = sim.run(qc, shots=1024).result()
        elapsed = (time.perf_counter() - start) * 1e3
        counts = result.get_counts()
        most_likely = max(counts, key=counts.get)
        found_index = int(most_likely, 2)
        return found_index, iterations, elapsed, counts

    # Run multiple qubit sizes
    grover_results = []
    for nq, tgt in [(2,2),(3,5),(4,11),(5,21)]:
        found, iters, elapsed, counts = grovers_search(nq, tgt)
        grover_results.append({
            'qubits': nq, 'db_size': 2**nq, 'target': tgt,
            'found': found, 'correct': found == tgt,
            'iterations': iters, 'time_ms': elapsed, 'counts': counts
        })
    
    # Primary result for display
    gr = grover_results[1]  # 3-qubit result
    gr_found, gr_iters, gr_time = gr['found'], gr['iterations'], gr['time_ms']
    gr_counts = gr['counts']
    grover_ok = True
except Exception as e:
    grover_ok = False
    gr_found, gr_iters, gr_time, gr_counts = 0, 0, 0, {}
    grover_results = []
    grover_error = str(e)

# Update experiments with actual quantum times
for exp in experiments:
    for gr_r in grover_results if grover_ok else []:
        if gr_r['db_size'] == exp['n']:
            exp['q_time_ms'] = gr_r['time_ms']

# ═══════════════════════════════════════════════════
# 4. GENERATE COMPARISON CHART
# ═══════════════════════════════════════════════════

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

sizes = [e['n'] for e in experiments]
cls_steps = [e['ls_steps'] for e in experiments]
bf_steps_list = [e['bf_steps'] for e in experiments]
q_steps = [e['q_iters'] for e in experiments]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
fig.patch.set_facecolor('#0f0f1a')

for ax in [ax1, ax2]:
    ax.set_facecolor('#0f0f1a')
    ax.tick_params(colors='#94a3b8')
    ax.xaxis.label.set_color('#94a3b8')
    ax.yaxis.label.set_color('#94a3b8')
    ax.title.set_color('#e2e8f0')
    for spine in ax.spines.values():
        spine.set_color('#1e293b')

ax1.plot(sizes, cls_steps, 'o-', label='P: Linear O(n)', color='#22c55e', lw=2)
ax1.plot(sizes, bf_steps_list, 's--', label='NP: Brute Force O(n²)', color='#f97316', lw=2)
ax1.plot(sizes, q_steps, '^-', label="Quantum: Grover O(√n)", color='#a855f7', lw=2)
ax1.set_xlabel('Input Size (n)')
ax1.set_ylabel('Steps / Iterations')
ax1.set_title('Steps Comparison (Log Scale)')
ax1.legend(facecolor='#1a1a2e', edgecolor='#334155', labelcolor='#e2e8f0')
ax1.set_yscale('log')
ax1.grid(True, alpha=0.15, color='#475569')

cls_times = [e['ls_time'] for e in experiments]
bf_times = [e['bf_time'] for e in experiments]
ax2.plot(sizes, cls_times, 'o-', label='P: Linear Search', color='#22c55e', lw=2)
ax2.plot(sizes, bf_times, 's--', label='NP: Brute Force', color='#f97316', lw=2)
ax2.set_xlabel('Input Size (n)')
ax2.set_ylabel('Execution Time (µs)')
ax2.set_title('Execution Time Comparison')
ax2.legend(facecolor='#1a1a2e', edgecolor='#334155', labelcolor='#e2e8f0')
ax2.grid(True, alpha=0.15, color='#475569')

plt.tight_layout()
chart_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'comparison_chart.png')
plt.savefig(chart_path, dpi=150, bbox_inches='tight', facecolor='#0f0f1a')
plt.close()

with open(chart_path, 'rb') as f:
    chart_b64 = base64.b64encode(f.read()).decode()

# ═══════════════════════════════════════════════════
# 5. BUILD HTML REPORT
# ═══════════════════════════════════════════════════

# Primary single-run results for cards
main = experiments[4]  # n=64

# Build experimentation table rows
table_rows = ""
for e in experiments:
    q_time_str = f"{e.get('q_time_ms', '-'):.2f} ms" if 'q_time_ms' in e else f"~{e['q_iters']} iters"
    table_rows += f"""<tr>
      <td>{e['n']}</td><td>{e['ls_steps']}</td><td>{e['ls_time']:.1f} µs</td>
      <td>{e['bf_steps']:,}</td><td>{e['bf_time']:.1f} µs</td>
      <td>{e['q_iters']}</td><td>{q_time_str}</td>
    </tr>"""

# Grover multi-qubit table
grover_table = ""
for r in grover_results:
    grover_table += f"""<tr>
      <td>{r['qubits']}</td><td>{r['db_size']}</td><td>{r['target']}</td>
      <td>{r['found']}</td><td>{'✅' if r['correct'] else '❌'}</td>
      <td>{r['iterations']}</td><td>{r['time_ms']:.2f} ms</td>
    </tr>"""

# Grover bar chart
bar_html = ""
if gr_counts:
    max_count = max(gr_counts.values())
    for k, v in sorted(gr_counts.items()):
        is_target = int(k, 2) == 5
        cls = "target" if is_target else ""
        pct = v / max_count * 100 if max_count > 0 else 0
        bar_html += f'''<div class="bar-wrapper">
          <div class="bar-count">{v}</div>
          <div class="bar {cls}" style="height:{pct}%"></div>
          <div class="bar-label">|{k}⟩</div>
        </div>'''

timestamp = time.strftime('%B %d, %Y at %I:%M %p')

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>P vs NP vs Quantum — TOC Project Results</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:'Inter',sans-serif;background:#0a0a0f;color:#e2e8f0;min-height:100vh;overflow-x:hidden}}
body::before{{content:'';position:fixed;top:-50%;left:-50%;width:200%;height:200%;
  background:radial-gradient(circle at 30% 20%,rgba(99,102,241,.08) 0%,transparent 50%),
  radial-gradient(circle at 70% 80%,rgba(168,85,247,.06) 0%,transparent 50%),
  radial-gradient(circle at 50% 50%,rgba(34,197,94,.04) 0%,transparent 60%);
  z-index:-1;animation:bgShift 20s ease-in-out infinite alternate}}
@keyframes bgShift{{0%{{transform:translate(0,0)}}100%{{transform:translate(-5%,3%)}}}}
.container{{max-width:1200px;margin:0 auto;padding:2rem 1.5rem 4rem}}
header{{text-align:center;padding:3rem 0 1rem}}
header h1{{font-size:2.4rem;font-weight:800;background:linear-gradient(135deg,#818cf8,#a855f7,#22c55e);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;margin-bottom:.5rem}}
header p{{color:#94a3b8;font-size:1.05rem}}
header .subtitle{{color:#64748b;font-size:.85rem;margin-top:.3rem}}
.cards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:1.5rem;margin-top:2rem}}
.card{{background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.06);border-radius:16px;
  padding:1.8rem;backdrop-filter:blur(12px);transition:transform .3s,border-color .3s,box-shadow .3s;position:relative;overflow:hidden}}
.card::before{{content:'';position:absolute;top:0;left:0;right:0;height:3px;border-radius:16px 16px 0 0}}
.card:hover{{transform:translateY(-4px);border-color:rgba(255,255,255,.12);box-shadow:0 20px 60px -15px rgba(0,0,0,.5)}}
.card.green::before{{background:linear-gradient(90deg,#22c55e,#4ade80)}}
.card.orange::before{{background:linear-gradient(90deg,#f97316,#fb923c)}}
.card.purple::before{{background:linear-gradient(90deg,#a855f7,#c084fc)}}
.badge{{display:inline-block;font-size:.7rem;font-weight:600;text-transform:uppercase;letter-spacing:.08em;
  padding:.25rem .7rem;border-radius:999px;margin-bottom:1rem}}
.card.green .badge{{background:rgba(34,197,94,.12);color:#4ade80}}
.card.orange .badge{{background:rgba(249,115,22,.12);color:#fb923c}}
.card.purple .badge{{background:rgba(168,85,247,.12);color:#c084fc}}
.card h2{{font-size:1.2rem;font-weight:700;margin-bottom:1rem}}
.stat-grid{{display:grid;grid-template-columns:1fr 1fr;gap:.8rem}}
.stat{{background:rgba(255,255,255,.03);border-radius:10px;padding:.8rem;text-align:center}}
.stat .label{{font-size:.7rem;color:#64748b;text-transform:uppercase;letter-spacing:.05em}}
.stat .value{{font-size:1.4rem;font-weight:700;margin-top:.2rem}}
.card.green .stat .value{{color:#4ade80}}
.card.orange .stat .value{{color:#fb923c}}
.card.purple .stat .value{{color:#c084fc}}
.complexity{{font-size:.85rem;color:#94a3b8;margin-top:1rem;padding-top:.8rem;border-top:1px solid rgba(255,255,255,.06)}}
.complexity span{{font-weight:600}}

.section{{margin-top:2.5rem;background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.06);
  border-radius:16px;padding:2rem;backdrop-filter:blur(12px)}}
.section h2{{font-size:1.3rem;font-weight:700;margin-bottom:1.5rem;
  background:linear-gradient(135deg,#818cf8,#a855f7);-webkit-background-clip:text;
  -webkit-text-fill-color:transparent;background-clip:text}}
.section h2.purple{{background:linear-gradient(135deg,#a855f7,#c084fc);-webkit-background-clip:text;background-clip:text}}
.section h2.green{{background:linear-gradient(135deg,#22c55e,#4ade80);-webkit-background-clip:text;background-clip:text}}
.section h2.orange{{background:linear-gradient(135deg,#f97316,#fb923c);-webkit-background-clip:text;background-clip:text}}
.section img{{max-width:100%;border-radius:12px;border:1px solid rgba(255,255,255,.06)}}
.section.center{{text-align:center}}

table{{width:100%;border-collapse:collapse;margin-top:1rem;font-size:.9rem}}
th{{background:rgba(99,102,241,.1);color:#a5b4fc;padding:.7rem .5rem;text-align:center;
  font-weight:600;font-size:.75rem;text-transform:uppercase;letter-spacing:.05em;
  border-bottom:2px solid rgba(99,102,241,.2)}}
td{{padding:.6rem .5rem;text-align:center;border-bottom:1px solid rgba(255,255,255,.04);color:#cbd5e1}}
tr:hover td{{background:rgba(255,255,255,.02)}}

.bar-chart{{display:flex;align-items:flex-end;gap:.6rem;height:200px;padding:0 1rem}}
.bar-wrapper{{flex:1;display:flex;flex-direction:column;align-items:center;gap:.3rem;height:100%;justify-content:flex-end}}
.bar{{width:100%;border-radius:6px 6px 0 0;background:linear-gradient(180deg,#a855f7,#7c3aed);
  transition:height 1s cubic-bezier(.34,1.56,.64,1);min-height:4px}}
.bar.target{{background:linear-gradient(180deg,#22c55e,#16a34a)}}
.bar-count{{font-size:.75rem;font-weight:600;color:#c084fc}}
.bar-label{{font-size:.75rem;color:#64748b;font-family:'Courier New',monospace}}

.analysis-grid{{display:grid;grid-template-columns:1fr 1fr;gap:1.5rem;margin-top:1rem}}
.analysis-item{{background:rgba(255,255,255,.02);border-radius:12px;padding:1.2rem;border-left:3px solid #818cf8}}
.analysis-item h3{{font-size:.95rem;font-weight:600;color:#a5b4fc;margin-bottom:.5rem}}
.analysis-item p{{font-size:.85rem;color:#94a3b8;line-height:1.6}}
.analysis-item.highlight{{border-left-color:#22c55e}}
.conclusion-box{{background:linear-gradient(135deg,rgba(34,197,94,.05),rgba(168,85,247,.05));
  border:1px solid rgba(34,197,94,.15);border-radius:12px;padding:1.5rem;margin-top:1rem}}
.conclusion-box p{{font-size:.9rem;color:#cbd5e1;line-height:1.7;margin-bottom:.5rem}}
.conclusion-box strong{{color:#4ade80}}

.footer{{text-align:center;margin-top:3rem;color:#475569;font-size:.8rem}}

@keyframes fadeUp{{from{{opacity:0;transform:translateY(20px)}}to{{opacity:1;transform:translateY(0)}}}}
.card,.section{{animation:fadeUp .6s ease-out backwards}}
.card:nth-child(1){{animation-delay:.1s}}.card:nth-child(2){{animation-delay:.2s}}.card:nth-child(3){{animation-delay:.3s}}

@media(max-width:768px){{
  .analysis-grid{{grid-template-columns:1fr}}
  header h1{{font-size:1.6rem}}
}}
</style>
</head>
<body>
<div class="container">
  <header>
    <h1>Experimental Study of P, NP & Quantum Computing</h1>
    <p>Theory of Computation — Unsorted Search Algorithm Comparison</p>
    <p class="subtitle">Problem: Search in Unsorted List | Tools: Python, Qiskit, AerSimulator</p>
  </header>

  <!-- Algorithm Result Cards -->
  <div class="cards">
    <div class="card green">
      <span class="badge">Class P</span>
      <h2>Linear Search</h2>
      <div class="stat-grid">
        <div class="stat"><div class="label">Index Found</div><div class="value">{main['ls_steps']}</div></div>
        <div class="stat"><div class="label">Steps</div><div class="value">{main['ls_steps']}</div></div>
        <div class="stat"><div class="label">Time</div><div class="value">{main['ls_time']:.1f}µs</div></div>
        <div class="stat"><div class="label">Input Size</div><div class="value">{main['n']}</div></div>
      </div>
      <div class="complexity">Complexity: <span>O(n)</span> — Scans each element sequentially until match found.</div>
    </div>

    <div class="card orange">
      <span class="badge">NP / Brute Force</span>
      <h2>Exhaustive Search</h2>
      <div class="stat-grid">
        <div class="stat"><div class="label">Index Found</div><div class="value">{main['n']//2}</div></div>
        <div class="stat"><div class="label">Steps</div><div class="value">{main['bf_steps']:,}</div></div>
        <div class="stat"><div class="label">Time</div><div class="value">{main['bf_time']:.1f}µs</div></div>
        <div class="stat"><div class="label">Input Size</div><div class="value">{main['n']}</div></div>
      </div>
      <div class="complexity">Complexity: <span>O(n²)</span> — Redundant nested loop simulating exhaustive NP-style check.</div>
    </div>

    <div class="card purple">
      <span class="badge">Quantum (BQP)</span>
      <h2>Grover's Algorithm</h2>
      <div class="stat-grid">
        <div class="stat"><div class="label">Target</div><div class="value">5</div></div>
        <div class="stat"><div class="label">Found</div><div class="value">{gr_found}</div></div>
        <div class="stat"><div class="label">Iterations</div><div class="value">{gr_iters}</div></div>
        <div class="stat"><div class="label">Time</div><div class="value">{gr_time:.1f}ms</div></div>
      </div>
      <div class="complexity">Complexity: <span>O(√n)</span> — Quantum amplitude amplification on 3-qubit (8-element) database.</div>
    </div>
  </div>

  <!-- Step 4: Experimentation Table -->
  <div class="section">
    <h2>📋 Step 4: Experimentation — Multi-Size Results Table</h2>
    <table>
      <tr><th>Input Size (n)</th><th>P Steps</th><th>P Time</th><th>NP Steps</th><th>NP Time</th><th>Quantum Iters</th><th>Quantum Time</th></tr>
      {table_rows}
    </table>
  </div>

  <!-- Grover Multi-Qubit Results -->
  <div class="section">
    <h2 class="purple">🔬 Grover's Algorithm — Multi-Qubit Experiments</h2>
    <table>
      <tr><th>Qubits</th><th>DB Size</th><th>Target</th><th>Found</th><th>Correct?</th><th>Iterations</th><th>Sim Time</th></tr>
      {grover_table}
    </table>
  </div>

  <!-- Comparison Chart -->
  <div class="section center">
    <h2>📊 Performance Comparison Charts</h2>
    <img src="data:image/png;base64,{chart_b64}" alt="P vs NP vs Quantum comparison chart">
  </div>

  <!-- Grover Measurement Distribution -->
  <div class="section">
    <h2 class="purple">🔬 Grover's Measurement Distribution (1024 shots, target |101⟩ = 5)</h2>
    <div class="bar-chart">{bar_html}</div>
  </div>

  <!-- Step 6: Analysis -->
  <div class="section">
    <h2 class="green">📝 Step 6: Analysis</h2>
    <div class="analysis-grid">
      <div class="analysis-item highlight">
        <h3>Which approach is faster?</h3>
        <p>For unsorted search, <strong style="color:#4ade80">Grover's Algorithm is the fastest</strong> in terms of 
        query complexity — O(√n) vs O(n) for classical. However, actual simulation time on classical hardware is 
        higher due to quantum circuit overhead.</p>
      </div>
      <div class="analysis-item">
        <h3>How does time increase with input size?</h3>
        <p><strong style="color:#4ade80">Linear (P):</strong> Grows linearly — doubling n roughly doubles steps.<br>
        <strong style="color:#fb923c">Brute Force (NP):</strong> Grows quadratically — doubling n quadruples steps.<br>
        <strong style="color:#c084fc">Quantum:</strong> Grows as √n — doubling n increases steps by only ~1.4x.</p>
      </div>
      <div class="analysis-item">
        <h3>Does quantum always outperform classical?</h3>
        <p><strong style="color:#c084fc">Not always in practice.</strong> Quantum simulation on classical hardware adds 
        overhead. For small inputs, classical is faster. The quantum advantage becomes significant for very large databases 
        where the O(√n) scaling dominates.</p>
      </div>
      <div class="analysis-item highlight">
        <h3>Why or why not?</h3>
        <p>Quantum computers use <strong style="color:#c084fc">superposition</strong> to evaluate multiple states simultaneously 
        and <strong style="color:#c084fc">amplitude amplification</strong> to boost the probability of the correct answer. 
        This gives a provable quadratic speedup. But current quantum hardware has noise and decoherence limitations.</p>
      </div>
    </div>
  </div>

  <!-- Step 7: Conclusion -->
  <div class="section">
    <h2 class="orange">🎯 Step 7: Conclusion</h2>
    <div class="conclusion-box">
      <p>📌 <strong>Problem:</strong> Searching for an element in an unsorted list.</p>
      <p>📌 <strong>Best Classical Approach:</strong> Linear Search (P-class) with O(n) complexity is the optimal 
      deterministic classical algorithm for unsorted search.</p>
      <p>📌 <strong>Brute Force (NP-style):</strong> The O(n²) exhaustive approach is significantly slower and 
      demonstrates why NP-hard problems are computationally expensive.</p>
      <p>📌 <strong>Quantum Advantage:</strong> Grover's Algorithm achieves O(√n) complexity — a proven quadratic speedup. 
      For a database of 1 million items, classical needs ~500,000 steps on average, while Grover's needs only ~785 iterations.</p>
      <p>📌 <strong>Key Insight:</strong> Quantum computing does not solve NP-complete problems in polynomial time, 
      but provides meaningful speedups for specific problems like unstructured search. The P vs NP question remains open.</p>
    </div>
  </div>

  <div class="footer">
    <p>Generated on {timestamp} — TOC Project by Dhruv</p>
    <p style="margin-top:.3rem">Tools: Python, Qiskit, AerSimulator, Matplotlib</p>
  </div>
</div>
</body>
</html>"""

output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results.html')
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"[OK] Report saved to: {output_path}")

import webbrowser
webbrowser.open(f'file:///{output_path.replace(os.sep, "/")}')
print("[OK] Opened in your default browser!")
