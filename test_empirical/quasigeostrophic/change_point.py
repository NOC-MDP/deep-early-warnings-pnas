import matplotlib.pyplot as plt
import ruptures as rpt
import pandas as pd


df = pd.read_csv(
    f"data/qg016.eng.csv",
    header=0,
    names=["Age", "Proxy", ],
)

# detection
algo = rpt.Pelt(model="rbf").fit(df["Proxy"][300:].values)
result = algo.predict(pen=25)

# display
rpt.display(df["Proxy"][300:], result, result)
plt.show()