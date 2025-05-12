import matplotlib.pyplot as plt
import ruptures as rpt
import pandas as pd
import numpy as np

def calculate_BIC(data, sensitivity, cal=None):
    if cal is None:
        cal = [6, 3, 1.5]
    if sensitivity == "Low":
        return cal[0] * np.log(len(data))
    elif sensitivity == "Medium":
        return cal[1] * np.log(len(data))
    elif sensitivity == "High":
        return cal[2] * np.log(len(data))

def calculate_MBIC(data, sensitivity, k, cal=None):
    if cal is None:
        cal = [12, 6, 3]
    if sensitivity == "Low":
        p = cal[0]
    elif sensitivity == "Medium":
        p = cal[1]
    elif sensitivity == "High":
        p = cal[2]
    else:
        raise Exception("Invalid sensitivity")

    return (p * (k + 1)+k) * np.log(len(data))/2

df = pd.read_csv(
    f"data/qg016.eng.csv",
    header=0,
    names=["Age", "Proxy", ],
)

signal = df["Proxy"][300:].values

pen = calculate_MBIC(signal, sensitivity="Low",k=5)

print(f"penalty = {pen}")

# detection
algo = rpt.Pelt(model="l2").fit(signal=signal)
my_bkps = algo.predict(pen=pen)

# display
rpt.display(signal, my_bkps, my_bkps)
plt.show()