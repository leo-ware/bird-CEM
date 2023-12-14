from sklearn.neighbors import KNeighborsRegressor
import pandas as pd

data = pd.read_csv('data/gen_data/pop_data.csv')

def pop_infer(lat, lon):
    if type(lat) == float:
        lat = [lat]
    if type(lon) == float:
        lon = [lon]
    
    knn = KNeighborsRegressor(n_neighbors=1)
    knn.fit(data[['lat', 'lon']], data['pop_density'])

    df = pd.DataFrame({'lat': lat, 'lon': lon})
    df['pop_density'] = knn.predict(df[['lat', 'lon']])
    return df
