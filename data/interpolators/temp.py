import pandas as pd
import numpy as np
from shapely.wkt import loads
from sklearn.neighbors import KNeighborsRegressor

cov = pd.read_csv("data/gen_data/temp_covariates.csv", index_col=0)
cov['geometry'] = cov['geometry'].apply(loads)

def temp_infer(lat, lon, n_neighbors=4, weights='distance'):
    lat = np.array(lat)
    lon = np.array(lon)
    
    cov['lat'] = cov['geometry'].apply(lambda x: x.y)
    cov['lon'] = cov['geometry'].apply(lambda x: x.x)

    models = {}
    for obj in ['avg_temp', 'avg_min_month', 'avg_max_month']:
        model = KNeighborsRegressor(n_neighbors=n_neighbors, weights=weights)
        model.fit(cov[['lat', 'lon']], cov[obj])
        models[obj] = model
    
    res = pd.DataFrame({'lat': lat, 'lon': lon})
    for obj in models:
        res[obj] = models[obj].predict(res[['lat', 'lon']])
    
    return res
