"""
Q7: Diagnose, redesign and validate OFDMA best-subcarrier starvation.
Python 3 + NumPy + pandas + Matplotlib.
Fixed seed; 8 users, 64 subcarriers, 1500 independent fading realisations.
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

SEED = 704
USERS, SUBCARRIERS, REALISATIONS = 8, 64, 1500
SNR_LINEAR = 8.0
MEAN_GAINS = np.array([1.00, 0.90, 0.78, 0.65, 0.52, 0.38, 0.22, 0.10])

def jain_index(values):
    values = np.asarray(values, dtype=float)
    return (values.sum() ** 2) / (len(values) * np.sum(values ** 2))

def main():
    rng = np.random.default_rng(SEED)
    # Exponential power gain represents Rayleigh small-scale fading.
    fading = rng.exponential(
        scale=1.0, size=(REALISATIONS, USERS, SUBCARRIERS)
    )
    channel_gain = fading * MEAN_GAINS[None, :, None]
    rate = np.log2(1.0 + SNR_LINEAR * channel_gain)

    original = np.zeros((REALISATIONS, USERS))
    redesigned = np.zeros((REALISATIONS, USERS))

    for r in range(REALISATIONS):
        # ORIGINAL: each subcarrier goes to the user with highest instantaneous rate.
        owner = np.argmax(rate[r], axis=0)
        for u in range(USERS):
            original[r, u] = rate[r, u, owner == u].sum()

        # REDESIGN: proportional-fair allocation.
        # Repeatedly choose the remaining user/subcarrier pair with greatest
        # instantaneous-rate / accumulated-throughput metric.
        accumulated = np.full(USERS, 0.05)  # small positive initial fairness state
        remaining = set(range(SUBCARRIERS))
        while remaining:
            best_pair, best_metric = None, -1.0
            for sc in remaining:
                user_metrics = rate[r, :, sc] / accumulated
                user = int(np.argmax(user_metrics))
                metric = float(user_metrics[user])
                if metric > best_metric:
                    best_metric = metric
                    best_pair = (user, sc)
            user, sc = best_pair
            redesigned[r, user] += rate[r, user, sc]
            accumulated[user] += rate[r, user, sc]
            remaining.remove(sc)

    original_mean = original.mean(axis=0)
    redesigned_mean = redesigned.mean(axis=0)

    summary = pd.DataFrame([
        {
            "strategy": "Original: maximum-rate",
            "sum_throughput": original_mean.sum(),
            "jain_fairness": jain_index(original_mean),
            "minimum_user_rate": original_mean.min(),
            "maximum_user_rate": original_mean.max(),
            "weakest_user_share_percent": 100 * original_mean[-1] / original_mean.sum()
        },
        {
            "strategy": "Redesign: proportional-fair",
            "sum_throughput": redesigned_mean.sum(),
            "jain_fairness": jain_index(redesigned_mean),
            "minimum_user_rate": redesigned_mean.min(),
            "maximum_user_rate": redesigned_mean.max(),
            "weakest_user_share_percent": 100 * redesigned_mean[-1] / redesigned_mean.sum()
        }
    ])
    per_user = pd.DataFrame({
        "user": [f"U{i+1}" for i in range(USERS)],
        "mean_channel_gain": MEAN_GAINS,
        "original_max_rate": original_mean,
        "redesigned_proportional_fair": redesigned_mean
    })
    raw_rows = []
    for r in range(REALISATIONS):
        for u in range(USERS):
            raw_rows.append({
                "realisation": r + 1,
                "user": f"U{u+1}",
                "mean_channel_gain": MEAN_GAINS[u],
                "original_rate": original[r, u],
                "redesigned_rate": redesigned[r, u]
            })
    raw = pd.DataFrame(raw_rows)

    summary.to_csv("q7_summary_metrics.csv", index=False)
    per_user.to_csv("q7_per_user_results.csv", index=False)
    raw.to_csv("q7_raw_experiment_data.csv", index=False)

    x = np.arange(USERS)
    width = 0.36
    plt.figure(figsize=(9, 4.6))
    plt.bar(x-width/2, original_mean, width, label="Original max-rate")
    plt.bar(x+width/2, redesigned_mean, width, label="Proportional-fair redesign")
    plt.xticks(x, per_user["user"])
    plt.ylabel("Mean throughput (bit/s/Hz per OFDM symbol)")
    plt.title("Per-user throughput under heterogeneous channel quality")
    plt.grid(axis="y", alpha=0.25)
    plt.legend()
    plt.tight_layout()
    plt.savefig("q7_per_user_throughput.png", dpi=180)
    plt.close()

    plt.figure(figsize=(8, 4.4))
    plt.bar(summary["strategy"], summary["jain_fairness"])
    plt.ylim(0, 1.05)
    plt.ylabel("Jain's fairness index")
    plt.title("Fairness before and after redesign")
    plt.xticks(rotation=8)
    plt.grid(axis="y", alpha=0.25)
    plt.tight_layout()
    plt.savefig("q7_fairness.png", dpi=180)
    plt.close()

    plt.figure(figsize=(8, 4.4))
    plt.bar(summary["strategy"], summary["sum_throughput"])
    plt.ylabel("Sum throughput (bit/s/Hz)")
    plt.title("Aggregate throughput trade-off")
    plt.xticks(rotation=8)
    plt.grid(axis="y", alpha=0.25)
    plt.tight_layout()
    plt.savefig("q7_sum_throughput.png", dpi=180)
    plt.close()

    print(summary.to_string(index=False))
    print(per_user.round(3).to_string(index=False))

if __name__ == "__main__":
    main()
