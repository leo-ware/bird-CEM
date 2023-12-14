import pandas as pd
import geopandas as gpd
import numpy as np
from tqdm import tqdm
from shapely.wkt import loads
from shapely import Point, MultiPoint
from sklearn.neighbors import KDTree

from data.interpolators.temp import temp_infer
from data.interpolators.population import pop_infer

borders = gpd.read_file('data/source_data/world-administrative-boundaries.geojson')
birds = pd.read_csv("data/gen_data/birds_top.csv")

def create_grid_points(country_code, grid_size):
    try:
        border = borders[borders.iso_3166_1_alpha_2_codes == country_code].geometry.iloc[0]
    except IndexError:
        raise ValueError("Country code not found")

    minx, miny, maxx, maxy = border.bounds
    x = np.arange(minx, maxx, grid_size)
    y = np.arange(miny, maxy, grid_size)
    xx, yy = np.meshgrid(x, y)

    multi = MultiPoint(np.vstack([xx.reshape(-1), yy.reshape(-1)]).T)
    multi_filt = border.intersection(multi)

    lon = np.array([p.x for p in multi_filt.geoms])
    lat = np.array([p.y for p in multi_filt.geoms])

    grid = pd.DataFrame({"lat": lat, "lon": lon})
    return grid

def assign_birds(lat, lon, countryCode):
    global birds
    assert countryCode in birds.countryCode.unique()
    birds = birds[birds.countryCode == countryCode]
    res = pd.DataFrame({'lat': lat, 'lon': lon})
    tree = KDTree(res[["lat", "lon"]])

    print("Matching birds to grid cells: ", end="")
    for spec in tqdm(np.unique(birds.species)):
        spec_locations = birds[birds.species == spec][['decimalLatitude', 'decimalLongitude']]
        closest_station = tree.query(spec_locations, k=1, return_distance=False)
        app = np.hstack([closest_station.reshape(-1), res.index.values.reshape(-1)])
        station_ids, counts = np.unique(app, return_counts=True)
        counts -= 1

        assert ((station_ids[1:] - station_ids[:-1]) == 1).all()
        assert station_ids[0] == 0

        res[spec] = counts

    return res

def make_grid(country_code, grid_size):
    grid = create_grid_points(country_code, grid_size)
    bds = assign_birds(grid.lat, grid.lon, country_code)
    temp = temp_infer(grid.lat, grid.lon)
    pop = pop_infer(grid.lat, grid.lon)
    return (temp
        .merge(pop, on=["lat", "lon"])
        .merge(bds, on=["lat", "lon"])
    )
