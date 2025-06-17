import netCDF4 as nc
import csv
import numpy as np
import os
import click
from loguru import logger


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

@click.command()
@click.option('--parameter',required=True,help="parameter to use in prediction")
@click.option("--region",default="Labrador_Sea",help="region to apply predictions")
@click.option("--grid_size",default=5,help="length of grid x and y to overlay region")
def create_csv(parameter:str,region:str,grid_size:int):
    logger.info("starting compilation of monthy mean data into csv files")
    logger.info(f"parameter requested: {parameter}")
    logger.info(f"region selected: {region}")

    directory = "/gws/nopw/j04/class_vol1/CLASS-MEDUSA/OUT_eORCA12/C001/monthly/"
    years = list(range(2000,2101,1))
    months = list(range(1,13,1))
    regions = ["Labrador_Sea","Irminger_Sea","West_Scotland"]

    if region not in regions:
        logger.error(f"{region} not in {regions}")
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

    parameters =  ["MLD", "DIN", "CHL", "ZOS", "TOS"]
    if parameter not in parameters:
        logger.error(f"{parameter} not in {parameters}")
        raise Exception(f"unknown parameter: {parameter}")

    if parameter == "CHL" or parameter == "DIN":
        grid = "ptrc_T"
    elif parameter == "MLD" or parameter == "TOS" or parameter == "ZOS":
        grid = "grid_T"
    else:
        raise Exception(f"unable to set grid type for parameter: {parameter}")

    lat_values = np.linspace(lat_min, lat_max, grid_size)
    lon_values = np.linspace(lon_min, lon_max, grid_size)
    first_time = True

    os.makedirs(f"{region}/data/{parameter}/", exist_ok=True)
    for lat0 in lat_values:
        for lon0 in lon_values:
            with open(f"{region}/data/{parameter}/{parameter}_{lat0}_{lon0}_monthly.csv", "w") as csvfile:
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
                            par = ds.variables["mldr10_1"][:]
                        elif parameter == "TOS":
                            par = ds.variables["tos"][:]
                        elif parameter == "ZOS":
                            par = ds.variables["zos"][:]
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


if __name__ == "__main__":
    create_csv()
