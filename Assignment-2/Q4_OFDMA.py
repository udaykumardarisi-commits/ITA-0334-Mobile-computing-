import numpy as np

rng = np.random.default_rng(404)
U, N, TRIALS, SNR = 8, 64, 1200, 8.0
methods = ("Fixed contiguous", "Interleaved", "Channel-aware max-rate", "Max-min reference")
totals = {m: np.zeros(U) for m in methods}

for _ in range(TRIALS):
    gains = rng.exponential(1.0, size=(U,N))
    rates = np.log2(1 + SNR*gains)
    allocations = {}
    allocations["Fixed contiguous"] = np.repeat(np.arange(U), N//U)
    allocations["Interleaved"] = np.tile(np.arange(U), N//U)
    allocations["Channel-aware max-rate"] = np.argmax(rates, axis=0)
    # Greedy max-min: repeatedly assign each subcarrier to user with lowest accumulated rate.
    alloc = np.zeros(N, dtype=int)
    current = np.zeros(U)
    for n in range(N):
        u = int(np.argmin(current))
        alloc[n] = u
        current[u] += rates[u,n]
    allocations["Max-min reference"] = alloc
    for name, alloc in allocations.items():
        for n,u in enumerate(alloc):
            totals[name][u] += rates[u,n] / TRIALS

print("Q4 - OFDMA SUBCARRIER ALLOCATION")
print("Method                   | Sum throughput | Jain fairness")
for name in methods:
    x = totals[name]
    jain = (x.sum()**2)/(U*np.sum(x*x))
    print(f"{name:24} | {x.sum():14.3f} | {jain:13.4f}")
print("\\nPer-user mean throughput (bit/s/Hz):")
for name in methods:
    print(name + ": " + ", ".join(f"{v:.2f}" for v in totals[name]))
