import netCDF4 as nc
import csv
import numpy as np
import plotly.graph_objects as go
import os


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
    directory = "/gws/nopw/j04/class_vol1/CLASS-MEDUSA/OUT_eORCA12/C001/monthly/"
    parameter = "DIN" # CHL DIN or MLD
    if parameter == "CHL" or parameter == "DIN":
        grid = "ptrc_T"
    elif parameter == "MLD":
        grid = "grid_T"
    else:
        raise Exception(f"unknown parameter {parameter}")
    years = list(range(2000,2101,1))
    months = list(range(1,13,1))
    lat_min = 57.00
    lat_max = 60.00
    lon_min = -57.00
    lon_max = -47.00
    lat_values = np.linspace(lat_min, lat_max, 5)
    lon_values = np.linspace(lon_min, lon_max, 5)
    first_time = True
    create_plot = True
    create_csv = False

    if create_csv:
        os.makedirs(f"{parameter}{os.sep}", exist_ok=True)
        for lat0 in lat_values:
            for lon0 in lon_values:
                with open(f"{parameter}{os.sep}{parameter}_{lat0}_{lon0}_monthly.csv", "w") as csvfile:
                    writer = csv.writer(csvfile)
                    header = ["x", parameter]
                    writer.writerow(header)
                    x = 1
                    for year in years:
                        for month in months:
                            datafile = f"{directory}/{year}/eORCA12_MED_UKESM_y{year}m{month:02}_{grid}.nc"
                            ds = nc.Dataset(datafile)
                            if parameter == "CHL":
                                par_chd = ds.variables["CHD"][:,0,:,:]
                                par_chn = ds.variables["CHN"][:,0,:,:]
                                par = par_chd + par_chn
                            elif parameter == "DIN":
                                par = ds.variables["DIN"][:, 0, :, :]
                            elif parameter == "MLD":
                                par = ds.variables["MLD"][:]
                            else:
                                raise Exception(f"unknown parameter {parameter}")
                            # these just need to be loaded once since they shouldn't change across datasets
                            if first_time:
                                nav_lat = ds.variables['nav_lat'][:]
                                nav_lon = ds.variables['nav_lon'][:]
                                i, j = find_closest_index(nav_lat, nav_lon, lat0, lon0)
                                first_time = False
                            par_pt = par[:,i, j]
                            writer.writerow([x,par_pt[0]])
                            x = x + 1
                first_time = True
                print(f"{parameter}_{lat0}_{lon0}_monthly.csv written successfully")

    if create_plot:
        fig = go.Figure()

        for lat0 in lat_values:
            for lon0 in lon_values:
                x_vals = []
                mld_pt = []
                try:
                    with open(f"{parameter}{os.sep}{parameter}_{lat0}_{lon0}_monthly.csv", "r") as csvfile:
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
    main()
