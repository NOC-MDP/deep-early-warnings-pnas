import matplotlib.pyplot as plt
import ruptures as rpt
import pandas as pd
import numpy as np

df = pd.read_csv(
    f"data/qg018.eng.csv",
    header=0,
    names=["Age", "Proxy", ],
)

signal = df["Proxy"][300:].values
# model to use and minimum size of change point
model = "l2"
min_size = 250
n = len(signal)

# Fit algorithm
algo = rpt.Pelt(model=model,min_size=min_size).fit(signal)

# Try several penalty values
penalties = np.linspace(1, 100, 20)  # example penalty range
results = []

for pen in penalties:
    bkps = algo.predict(pen=pen)
    k = len(bkps) - 1  # number of change points

    # Compute cost

    cost_func = rpt.costs.CostRbf().fit(signal)
    rss = sum(cost_func.error(start, end)
              for start, end in zip([0] + bkps[:-1], bkps))

    # MBIC-like penalty (simplified version)
    mbic_score = rss + np.log(n) * k  # or multiply by d if multivariate
    results.append((pen, mbic_score, bkps))

# Select the penalty with the lowest MBIC
best_pen, best_score, best_bkps = min(results, key=lambda x: x[1])


print(f"Best penalty: {best_pen}")
print(f"Best score: {best_score}")

# display
rpt.display(signal, best_bkps, best_bkps)
plt.show()