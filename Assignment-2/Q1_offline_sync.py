import random

def simulate(p, n=1000, seed=42):
    rng = random.Random(seed + int(p * 100))
    immediate_ok = immediate_lost = 0
    queue, delays = [], []
    for t in range(n):
        up = rng.random() < p
        if up:
            immediate_ok += 1
        else:
            immediate_lost += 1
        queue.append(t)
        if up:
            while queue:
                created = queue.pop(0)
                delays.append(t - created)
    t = n
    while queue:
        while rng.random() >= p:
            t += 1
        t += 1
        while queue:
            created = queue.pop(0)
            delays.append(t - created)
    return immediate_ok, immediate_lost, len(delays), sum(d > 0 for d in delays), sum(delays)/len(delays)

print("Q1 - OFFLINE STORE-AND-FORWARD SIMULATION")
print("Link | Immediate OK | Immediate lost | Queued delivered | Delayed | Mean delay")
for p in (0.90, 0.60, 0.30):
    a, b, c, d, e = simulate(p)
    print(f"{p:>4.0%} | {a:>12} | {b:>14} | {c:>15} | {d:>7} | {e:>9.3f} min")
