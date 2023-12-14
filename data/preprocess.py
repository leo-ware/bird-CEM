from sklearn.neighbors import KNeighborsRegressor
import pandas as pd
import numpy as np
import netCDF4 as nc
import geopandas as gpd
from shapely.geometry import Point

def temp():
    bnc = nc.Dataset('data/source_data/Complete_TAVG_LatLong1.nc', 'r')

    mlat, mlon = np.meshgrid(bnc.variables["latitude"][:], bnc.variables["longitude"][:])
    data = gpd.GeoDataFrame(geometry=[Point(x,y) for x,y in zip(mlon.reshape(-1), mlat.reshape(-1))])

    climatology = bnc.variables['climatology'][:]

    avg_temp = climatology.mean(axis=0)
    data['avg_temp'] = avg_temp.T.reshape(-1)
    avg_min_month = climatology.min(axis=0)
    data['avg_min_month'] = avg_min_month.T.reshape(-1)
    avg_max_month = climatology.max(axis=0)
    data['avg_max_month'] = avg_max_month.T.reshape(-1)

    data.dropna().to_csv('data/gen_data/temp_covariates.csv')


def birds():
    birds_full = pd.read_csv('data/source_data/birds.csv', sep="\t")

    birds = birds_full[["species", "decimalLatitude", "decimalLongitude", "countryCode", "year", "recordedBy"]]
    birds = birds.dropna()

    birds = birds[birds["year"] >= 2022].drop("year", axis=1)
    top_100_GB = set(birds[birds.countryCode == "GB"]
        .groupby("species").size().sort_values(ascending=False).head(100).index)

    birds_top = birds[birds.species.isin(top_100_GB)]
    birds_top.to_csv("data/gen_data/birds_top.csv", index=False)

def population_density():
    file = "data/source_data/gpw-v4/gpw_v4_population_density_rev11_30_min.nc"
    nc_data = nc.Dataset(file)

    lon = nc_data["longitude"][:]
    lat = nc_data["latitude"][:]
    latm, lonm = np.meshgrid(lon, lat)

    raster = nc_data['Population Density, v4.11 (2000, 2005, 2010, 2015, 2020): 30 arc-minutes']
    pop_2020 = np.array(raster[4,:,:])

    pop_data = pd.DataFrame()
    pop_data['lat'] = latm.flatten()
    pop_data['lon'] = lonm.flatten()
    pop_data['pop_density'] = pop_2020.flatten()

    pop_data = pop_data[pop_data.pop_density > pop_data.pop_density.min()]

    pop_data.to_csv("data/gen_data/pop_data.csv", index=False)

def preprocess():
    temp()
    birds()
    population_density()
