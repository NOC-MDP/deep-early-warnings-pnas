import plotly.graph_objects as go
import numpy as np
import csv

def plot_csv(parameter:str="TOS",region="Labrador_Sea",grid_size:int = 5):

    parameters =  ["MLD", "DIN", "CHL", "ZOS", "TOS"]
    if parameter not in parameters:
        raise Exception(f"unknown parameter: {parameter}")

    regions = ["Labrador_Sea","Irminger_Sea","West_Scotland"]

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

    lat_values = np.linspace(lat_min, lat_max, grid_size)
    lon_values = np.linspace(lon_min, lon_max, grid_size)

    fig = go.Figure()

    for lat0 in lat_values:
        for lon0 in lon_values:
            x_vals = []
            mld_pt = []
            try:
                with open(f"{region}/data/{parameter}/{parameter}_{lat0}_{lon0}_monthly.csv", "r") as csvfile:
                    reader = csv.reader(csvfile)
                    for row in reader:
                        try:
                            x_vals.append(int(row[0]))
                            mld_pt.append(float(row[1]))
                        except ValueError:
                            continue
                    fig.add_trace(go.Scatter(x=x_vals, y=mld_pt, name=f"{lat0}_{lon0}"))
            except FileNotFoundError:
                print(f"{parameter}_{lat0}_{lon0}_monthly.csv not found")
                continue
    fig.show()

if __name__ == "__main__":
    plot_csv()