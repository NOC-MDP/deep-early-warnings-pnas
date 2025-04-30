import netCDF4 as nc
import csv
# change prefix for relevent model run
prefix = "qg018"
data_file = f"{prefix}.eng.nc"

ds = nc.Dataset(data_file)

ke = ds.variables["kinetic_energy"][:]
#ts = ds.variables["transport"][:]

with open(f"{prefix}.eng.csv", "w") as csvfile:
    writer = csv.writer(csvfile)
    header = ["x","kinetic_energy"]
    writer.writerow(header)
    x = 1
    #assert ke.__len__() == ts.__len__()
    for i in range(ke.__len__()):
        writer.writerow([x,ke[i]])
        x = x + 1