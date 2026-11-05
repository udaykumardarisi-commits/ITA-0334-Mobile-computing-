import numpy as np

def array_factor(N, theta_deg, steer_deg=0):
    theta = np.radians(theta_deg)
    steer = np.radians(steer_deg)
    n = np.arange(N)
    phase = 2*np.pi*0.5*n[:,None]*(np.sin(theta)[None,:]-np.sin(steer))
    af = np.abs(np.sum(np.exp(1j*phase),axis=0))/N
    return 20*np.log10(np.maximum(af,1e-8))

angles = np.linspace(-90,90,3601)
print("Q5 - SDMA UNIFORM LINEAR ARRAY BEAM ANALYSIS")
print("Elements | Approx. HPBW (deg) | First-null estimate (deg) | 10 dB separation")
for N in (2,4,8,16):
    db = array_factor(N, angles)
    peak = np.argmax(db)
    half = np.where(db >= -3)[0]
    hpbw = angles[half[-1]] - angles[half[0]]
    nulls = np.where((db[1:-1] < db[:-2]) & (db[1:-1] < db[2:]))[0] + 1
    positive_nulls = [angles[i] for i in nulls if angles[i] > 0.1]
    first_null = positive_nulls[0] if positive_nulls else float("nan")
    idx = np.where(db <= -10)[0]
    sep = angles[idx[idx > peak][0]] if np.any(idx > peak) else float("nan")
    print(f"{N:8} | {hpbw:18.2f} | {first_null:23.2f} | {sep:15.2f}")
print("\\nModel: half-wavelength ULA; values are array-pattern estimates, not full cellular SINR.")
