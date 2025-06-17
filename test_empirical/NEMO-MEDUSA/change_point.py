import json
import subprocess

import ruptures as rpt
import pandas as pd
import numpy as np

parameter = "ZOS"
units = "metres" # "degC" mmol-N/m2 mmol-Chl/m2 metres
region = "Labrador_Sea"
grid_size = 5

parameters = ["MLD", "DIN", "CHL", "ZOS", "TOS"]
if parameter not in parameters:
    raise Exception(f"unknown parameter: {parameter}")

regions = ["Labrador_Sea", "Irminger_Sea", "West_Scotland"]

if region not in regions:
    raise Exception(f"unknown region: {region}")

if region == "Labrador_Sea":
    lat_min = 57.00
    lat_max = 60.00
    lon_min = -57.00
    lon_max = -47.00
elif region == "Irminger_Sea":
    lat_min = 58.00
    lat_max = 63.00
    lon_min = -40.00
    lon_max = -32.00
elif region == "West_Scotland":
    lat_min = 56.00
    lat_max = 61.00
    lon_min = -18.00
    lon_max = -8.00
else:
    raise Exception(f"unable to assign region extent to region: {region}")
first_bkps = []
lat_values = np.linspace(lat_min, lat_max, grid_size)
lon_values = np.linspace(lon_min, lon_max, grid_size)
transitions = {"transitions": []}
j = 1
skipped_points = 0
for lat0 in lat_values:
    for lon0 in lon_values:
        df = pd.read_csv(
            f"{region}/data/{parameter}/{parameter}_{lat0}_{lon0}_monthly.csv",
            header=0,
            names=["Age", "Proxy", ],
        )

        signal = df["Proxy"][:].values
        # model to use and minimum size of change point
        model = "l1"
        min_size = 240
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
        print(f"First Break Point: {best_bkps[0]}")

        # plot only the first breakpoint detected
        fig, axes = rpt.display(signal, [best_bkps[0],int(df["Age"].iloc[-1])], [best_bkps[0],int(df["Age"].iloc[-1])])
        axes[0].set_title(f"lat: {lat0} lon: {lon0}")
        axes[0].set_xlabel("Time: Days")
        axes[0].set_ylabel(f"{units}")
        fig.set_size_inches(10,2.25)
        fig.tight_layout()
        fig.show()
        fig.savefig(f"{region}/data/{parameter}/{region}_{parameter}_{lat0}_{lon0}.png")
        if int(df["Age"].iloc[-1]) == int(best_bkps[0]):
            print(f"no break points found for tsid {j} skipping")
            skipped_points = skipped_points + 1
        else:
            transistion = {
                "run_id": f"{lat0}_{lon0}",
                "start_age": int(df["Age"].iloc[0]),
                "end_age": int(df["Age"].iloc[-1]),
                "transition": int(best_bkps[0]),
                "tsid": j
            }
            transitions["transitions"].append(transistion)
            j = j +1

with open(f"{region}/data/{parameter}/{region}_{parameter}_transitions.json","w") as f:
    json.dump(transitions,f)
print(f"number of points skipped: {skipped_points}")

subprocess.Popen(["magick", "montage", f"{region}/data/{parameter}/{region}_{parameter}_*.png",
                  "-tile", "4x", "-geometry", "+10+10", "-title", f"{region}: {parameter} change points",
                  f"{region}/data/{parameter}/{parameter}_{region}_combined.png"])