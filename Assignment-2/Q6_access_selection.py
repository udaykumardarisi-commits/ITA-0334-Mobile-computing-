import numpy as np

criteria = ["Spectral efficiency","Interference/reuse","Robustness","Scalability","Latency/QoS","Cost"]
weights = np.array([.25,.20,.20,.15,.10,.10])
ratings = {
 "Cellular voice": {"SDMA":[4,4,4,4,3,3],"TDMA":[3,3,4,3,4,4],"FDMA":[2,3,4,2,4,4],"CDMA":[4,4,4,4,4,2],"OFDMA":[5,4,4,5,5,3]},
 "Tactical": {"SDMA":[3,3,3,3,3,3],"TDMA":[3,3,4,3,4,4],"FDMA":[2,3,4,2,4,4],"CDMA":[4,4,4,4,4,3],"OFDMA":[4,4,3,4,4,3]},
 "Stadium": {"SDMA":[5,4,4,4,4,3],"TDMA":[3,3,3,3,3,4],"FDMA":[2,3,3,2,3,4],"CDMA":[3,3,3,3,3,3],"OFDMA":[5,4,4,5,5,3]},
 "5000 sensors": {"SDMA":[3,3,4,3,3,3],"TDMA":[3,3,4,4,4,4],"FDMA":[2,3,4,2,3,4],"CDMA":[3,4,4,4,3,3],"OFDMA":[4,4,4,5,4,3]}
}
print("Q6 - WEIGHTED ACCESS-TECHNIQUE DECISION")
print("Scenario       | " + " | ".join(f"{k:5}" for k in ["SDMA","TDMA","FDMA","CDMA","OFDMA"]) + " | Winner")
for scenario, methods in ratings.items():
    scores = {m: float(np.dot(weights,np.array(v))) for m,v in methods.items()}
    winner = max(scores,key=scores.get)
    print(f"{scenario:14} | " + " | ".join(f"{scores[m]:5.2f}" for m in ["SDMA","TDMA","FDMA","CDMA","OFDMA"]) + f" | {winner}")
print("\\nWeights:", dict(zip(criteria,weights)))
