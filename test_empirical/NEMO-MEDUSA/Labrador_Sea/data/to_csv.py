import netCDF4 as nc
import csv
import numpy as np
import plotly.graph_objects as go

def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculate the great-circle distance between two points in degrees."""
    R = 6371.0  # Earth radius in km
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (np.sin(dlat / 2.0) ** 2 +
         np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2.0) ** 2)
    c = 2 * np.arcsin(np.sqrt(a))
    return R * c


def find_closest_index(lat_array, lon_array, lat0, lon0):
    """Find the i, j index of the closest point to (lat0, lon0)."""
    dist = haversine_distance(lat_array, lon_array, lat0, lon0)
    index = np.unravel_index(np.argmin(dist), lat_array.shape)
    return index

def main():

    datafile = "MLD_maxes2000-2100.nc"
    ds = nc.Dataset(datafile)
    mld = ds.variables['mldr10_1'][:]
    nav_lat = ds.variables['nav_lat'][:]
    nav_lon = ds.variables['nav_lon'][:]
    time_counter = ds.variables['time_counter'][:]
    lat_min = 57.00
    lat_max = 60.00
    lon_min = -57.00
    lon_max = -47.00
    lat_values = np.linspace(lat_min, lat_max, 5)
    lon_values = np.linspace(lon_min, lon_max, 5)
    x_vals = np.arange(1,time_counter.__len__()+1,1)
    fig = go.Figure()
    for lat0 in lat_values:
        for lon0 in lon_values:

            i, j = find_closest_index(nav_lat, nav_lon, lat0, lon0)

            mld_pt = mld[:,i, j]

            fig.add_trace(go.Scatter(x=x_vals, y=mld_pt,name=f"{lat0}_{lon0}"))

            with open(f"mldr10_1_{lat0}_{lon0}.csv", "w") as csvfile:
                writer = csv.writer(csvfile)
                header = ["x","MLD"]
                writer.writerow(header)
                x = 1
                for i in range(mld_pt.__len__()):
                    writer.writerow([x_vals[i],mld_pt[i]])
                    x = x + 1
    fig.show()

if __name__ == "__main__":
    main()