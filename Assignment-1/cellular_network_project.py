"""ITA0334 Mobile Computing Assignment 1: educational cellular-network simulator.
Run: pip install numpy matplotlib
     python cellular_network_project.py
Outputs are written to cellular_results/. Models are simplified; see README.txt.
"""
import math, csv, os
import numpy as np
import matplotlib.pyplot as plt

AREA=12.0; R=0.5; CHANNELS=336; TRAFFIC_PER_USER=0.025
GOS=0.02; TARGET_SIR_DB=12.0; N_CLUSTER=7; SECTORS=3
SUBSCRIBERS=[1000,10000,20000,100000]
OUT='cellular_results'; os.makedirs(OUT,exist_ok=True)
np.random.seed(42)

def erlang_b(c,a):
    b=1.0
    for k in range(1,c+1): b=a*b/(k+a*b)
    return b

def inverse_erlang_b(c,target=GOS):
    lo,hi=0.0,1000.0
    for _ in range(100):
        mid=(lo+hi)/2
        if erlang_b(c,mid)>target: hi=mid
        else: lo=mid
    return (lo+hi)/2

def cell_area(r): return 3*math.sqrt(3)*r*r/2
def reuse_distance(r,n): return r*math.sqrt(3*n)
def valid_clusters(m=12):
    return sorted({i*i+i*j+j*j for i in range(m+1) for j in range(m+1) if i*i+i*j+j*j>0})
def sir_theory(n,pathloss): return 10*math.log10((3*n)**(pathloss/2)/6)
def min_cluster(pathloss,target=TARGET_SIR_DB):
    return next((n for n in valid_clusters() if sir_theory(n,pathloss)>=target),None)
def hex_grid(rings=2):
    cells=[]
    for q in range(-rings,rings+1):
        for s in range(-rings,rings+1):
            t=-q-s
            if max(abs(q),abs(s),abs(t))<=rings:
                cells.append((q,s,1.5*R*q,math.sqrt(3)*R*(s+q/2)))
    return cells

def monte_carlo_sir(pathloss=4.0,samples=5000,cluster=N_CLUSTER,sectorized=False):
    theta=np.random.uniform(0,2*np.pi,samples)
    rad=R*np.sqrt(np.random.uniform(0,1,samples))
    ux,uy=rad*np.cos(theta),rad*np.sin(theta)
    ds=np.maximum(np.hypot(ux,uy),0.02)
    signal=ds**(-pathloss); interference=np.zeros(samples)
    for k in range(6):
        if sectorized and k not in (0,3): continue
        a=k*np.pi/3; bx=reuse_distance(R,cluster)*np.cos(a); by=reuse_distance(R,cluster)*np.sin(a)
        di=np.hypot(bx-ux,by-uy)
        interference+=di**(-pathloss)
    return 10*np.log10(signal/interference)

# Geometry / channel / Erlang capacity
Ac=cell_area(R); cells=math.ceil(AREA/Ac); q=math.sqrt(3*N_CLUSTER)
ch_cell=CHANNELS//N_CLUSTER; ch_sector=ch_cell//SECTORS
traffic_sector=inverse_erlang_b(ch_sector); traffic_cell=traffic_sector*SECTORS
network_capacity=traffic_cell*cells
print('\nTASK 3 - GEOMETRY AND CAPACITY')
print(f'Cell area={Ac:.4f} km^2; cells={cells}; N={N_CLUSTER}; D={reuse_distance(R,N_CLUSTER):.4f} km; Q={q:.4f}')
print(f'Channels/cell={ch_cell}; channels/sector={ch_sector}; Erlangs/sector at 2%={traffic_sector:.3f}')
print(f'Erlangs/cell={traffic_cell:.3f}; estimated network capacity={network_capacity:.2f} E')
print('\nTASK 3 - THEORETICAL SIR AND MINIMUM CLUSTER')
for p in [2.5,3.0,4.0]: print(f'n={p}: SIR(N=7)={sir_theory(7,p):.2f} dB; minimum N for 12 dB={min_cluster(p)}')

# Task 4: Monte Carlo user-position SIR statistics
sir=monte_carlo_sir(4.0,5000,N_CLUSTER)
print('\nTASK 4 - POSITION / SIR DISTRIBUTION')
print(f'Mean={np.mean(sir):.2f} dB; 5th percentile={np.percentile(sir,5):.2f} dB; 95th percentile={np.percentile(sir,95):.2f} dB; outage <12 dB={np.mean(sir<12)*100:.2f}%')

# Task 5/8: strategy load comparison (dynamic pooling is an ideal upper bound)
rows=[]
print('\nTASK 5 / 8 - GROWTH AND STRATEGY BLOCKING')
for users in SUBSCRIBERS:
    total=users*TRAFFIC_PER_USER; percell=total/cells; persector=percell/SECTORS
    vals={'Subscribers':users,'Offered_Erlang':total,
          'Fixed_reuse_blocking':erlang_b(ch_cell,percell),
          'Sectorised_blocking':erlang_b(ch_sector,persector),
          'Ideal_pool_blocking':erlang_b(CHANNELS,total),
          'One_split_round_blocking':erlang_b(ch_cell,percell/4)}
    rows.append(vals)
    print(f"{users:>7,} users, traffic={total:.2f} E; fixed={vals['Fixed_reuse_blocking']*100:.3f}%; sector={vals['Sectorised_blocking']*100:.3f}%; ideal pool={vals['Ideal_pool_blocking']*100:.3f}%; after split={vals['One_split_round_blocking']*100:.3f}%")
with open(os.path.join(OUT,'strategy_results.csv'),'w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)

# Task 6/7: uniform four-way splitting
print('\nTASK 6 / 7 - CELL SPLITTING RECURRENCE')
for k in range(5): print(f'Round {k}: cells={cells*4**k}; idealised capacity={network_capacity*4**k:.2f} E; relative power for n=4={1/(2**(4*k)):.6f}')
need=100000*TRAFFIC_PER_USER
rounds=max(0,math.ceil(math.log(need/network_capacity,4))) if need>network_capacity else 0
print(f'100,000-user traffic={need:.2f} E; uniform split rounds by aggregate capacity estimate={rounds}')

# Task 8: cluster/pathloss/sector test matrix
print('\nTASK 8 - SIMULATION TEST MATRIX')
for p in [2.5,3.0,4.0]:
    for n in [3,4,7,12]:
        a=monte_carlo_sir(p,1000,n,False); b=monte_carlo_sir(p,1000,n,True)
        print(f'N={n:2d}, pathloss={p}: omni mean={np.mean(a):.2f} dB; simplified sector mean={np.mean(b):.2f} dB')

# Task 9: plots
x=[r['Subscribers'] for r in rows]
plt.figure(); plt.plot(x,[r['Offered_Erlang'] for r in rows],marker='o'); plt.xlabel('Subscribers'); plt.ylabel('Offered traffic (Erlang)'); plt.title('Traffic growth'); plt.grid(True); plt.savefig(os.path.join(OUT,'traffic_growth.png'),dpi=160); plt.close()
plt.figure()
for key,label in [('Fixed_reuse_blocking','Fixed reuse'),('Sectorised_blocking','Sectorised'),('Ideal_pool_blocking','Ideal pooled upper bound'),('One_split_round_blocking','One split round')]: plt.plot(x,[r[key]*100 for r in rows],marker='o',label=label)
plt.xlabel('Subscribers'); plt.ylabel('Blocking probability (%)'); plt.title('Blocking vs subscriber growth'); plt.legend(); plt.grid(True); plt.savefig(os.path.join(OUT,'blocking_comparison.png'),dpi=160); plt.close()
plt.figure()
for p in [2.5,3.0,4.0]:
    z=np.sort(monte_carlo_sir(p,5000,N_CLUSTER)); plt.plot(z,np.arange(1,len(z)+1)/len(z),label=f'n={p}')
plt.axvline(12,ls='--',label='12 dB target'); plt.xlabel('SIR (dB)'); plt.ylabel('CDF'); plt.title('Monte Carlo SIR CDF'); plt.legend(); plt.grid(True); plt.savefig(os.path.join(OUT,'sir_cdf.png'),dpi=160); plt.close()

# Task 10: theory versus simulation
print('\nTASK 10 - THEORY VS SIMULATION')
theory=sir_theory(7,4); sim=float(np.mean(sir)); print(f'Theoretical SIR={theory:.2f} dB; simulated mean SIR={sim:.2f} dB; absolute difference={abs(theory-sim):.2f} dB')

# Task 11: design recommendation
print('\nTASK 11 - DESIGN RECOMMENDATION')
print('Baseline: N=7, 120-degree sectorisation, R=0.5 km; add small cells/temporary capacity in hotspots. Validate SIR by detailed RF planning.')

# Task 12: event traffic
print('\nTASK 12 - STADIUM EVENT')
event=25000*0.05; background=(100000*TRAFFIC_PER_USER/AREA)*1.0; combined=event+background
zone_capacity=network_capacity/AREA; cell_equiv=math.ceil(combined/traffic_cell)
print(f'Event traffic={event:.2f} E; background in 1 km^2={background:.2f} E; combined={combined:.2f} E')
print(f'Uniform-share zone capacity estimate={zone_capacity:.2f} E; capacity-equivalent cells required={cell_equiv}')
plt.figure(); plt.bar(['Normal zone share','Event only','Combined'],[zone_capacity,event,combined]); plt.ylabel('Traffic (Erlang)'); plt.title('Stadium event traffic assessment'); plt.grid(axis='y'); plt.savefig(os.path.join(OUT,'stadium_event.png'),dpi=160); plt.close()

# Save a text run summary
print('\nPROJECT COMPLETE. Files saved in:',OUT)
print('strategy_results.csv, traffic_growth.png, blocking_comparison.png, sir_cdf.png, stadium_event.png')
