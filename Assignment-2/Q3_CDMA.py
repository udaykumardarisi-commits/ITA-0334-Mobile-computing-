import numpy as np

def hadamard(L):
    H = np.array([[1.0]])
    while H.shape[0] < L:
        H = np.block([[H, H], [H, -H]])
    return H

def simulate(L, mode, nbits=2500, seed=19):
    rng = np.random.default_rng(seed + L + (0 if mode=="walsh" else 1))
    K = min(8, L)
    codes = hadamard(L)[:K] if mode in ("walsh", "nearfar") else rng.choice([-1.0,1.0],(K,L))
    bits = rng.choice([-1.0,1.0],(K,nbits))
    powers = np.ones(K)
    if mode == "nearfar":
        powers[-1] = 10.0
    errors = 0
    unit_codes = codes / np.sqrt(L)
    for i in range(nbits):
        rx = np.sum(np.sqrt(powers)[:,None] * bits[:,i,None] * unit_codes, axis=0)
        rx += rng.normal(0,0.22,L)
        detected = np.where(unit_codes @ rx >= 0, 1.0, -1.0)
        errors += np.count_nonzero(detected != bits[:,i])
    corr = unit_codes @ unit_codes.T
    off = corr - np.eye(K)
    return errors, errors/(K*nbits), np.max(np.abs(off))

print("Q3 - DS-CDMA SPREADING AND DESPREADING")
print("Length | Mode       | Users | Errors | BER       | Max cross-correlation")
for L in (8,16,64):
    for mode in ("walsh","random","nearfar"):
        e,ber,c=simulate(L,mode)
        print(f"{L:6} | {mode:10} | {min(8,L):5} | {e:6} | {ber:9.6f} | {c:21.6f}")
print("\\nProcessing gain:")
for L in (8,16,64):
    print(f"L={L:2}: {10*np.log10(L):.2f} dB")
