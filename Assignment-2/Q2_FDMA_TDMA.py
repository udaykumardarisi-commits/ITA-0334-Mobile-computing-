import numpy as np

def simulate(mode, traffic, seed=22, minutes=120):
    rng = np.random.default_rng(seed + (0 if mode == "FDMA" else 1))
    capacity = 74 if mode == "FDMA" else 60
    active = []
    accepted = blocked = occupied_resource_minutes = 0

    for minute in range(minutes):
        # Release calls/data sessions whose holding time has expired.
        active = [end for end in active if end > minute]
        if traffic == "continuous voice":
            arrivals = rng.poisson(18)
            durations = rng.integers(2, 5, arrivals)
        elif traffic == "bursty data":
            rate = 3 if minute % 10 else 24
            arrivals = rng.poisson(rate)
            durations = rng.integers(1, 2, arrivals)
        else:  # 70% voice-like sessions and 30% short data sessions
            arrivals = rng.poisson(15)
            durations = np.where(rng.random(arrivals) < 0.70,
                                 rng.integers(2, 5, arrivals),
                                 rng.integers(1, 2, arrivals))

        for duration in durations:
            if len(active) < capacity:
                active.append(minute + int(duration))
                accepted += 1
            else:
                blocked += 1
        occupied_resource_minutes += len(active)

    utilisation = occupied_resource_minutes / (minutes * capacity) * 100
    return accepted, blocked, utilisation, 100-utilisation

print("Q2 - FDMA vs TDMA DEDICATED RESOURCE SIMULATION")
print("Traffic            Access | Capacity | Accepted | Blocked | Utilisation | Unused")
for traffic in ("continuous voice", "bursty data", "70/30 mixed"):
    for mode in ("FDMA", "TDMA"):
        a,b,c,d = simulate(mode, traffic)
        cap = 74 if mode == "FDMA" else 60
        print(f"{traffic:18} {mode:5} | {cap:8} | {a:8} | {b:7} | {c:10.2f}% | {d:6.2f}%")
