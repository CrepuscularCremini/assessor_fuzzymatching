import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

fdf = pd.read_csv('FinalLightBox/final_light_box_parcels.csv')
fdf.head()
denver_uids = fdf[fdf.geom_id.str.contains('DE')].uid.unique().tolist()

p_df = pd.read_csv('{0}/{0}_propertypoints.csv'.format('08031'))
p_df.reset_index(inplace = True, drop = True)
p_df.reset_index(inplace = True)
p_df.rename(columns = {'index' : 'uid'}, inplace = True)
# p_df.columns.tolist()

j_p_df = p_df[['PROPERTY_ID', 'uid']]

with open('08031/Propertypoints_08031.csv', 'r') as file:
    full_den = pd.read_csv(file)
gdf = full_den.merge(j_p_df, on = 'PROPERTY_ID')

ogd = gdf.query('uid not in @denver_uids').copy()
out_columns = ['PARCEL_APN', 'SITE_ADDR','SITE_HOUSE_NUMBER','SITE_DIRECTION','SITE_STREET_NAME','SITE_MODE','SITE_CARRIER_CODE','SITE_QUADRANT','SITE_UNIT_PREFIX','SITE_UNIT_NUMBER','SITE_CITY','SITE_STATE','SITE_ZIP','SITE_PLUS_4','_X_COORD','_Y_COORD', 'geometry']
ogd['geometry'] = ogd.apply(lambda r: Point(r._X_COORD, r._Y_COORD), axis = 1)
g = gpd.GeoDataFrame(ogd[out_columns], geometry = 'geometry', crs = 'EPSG:4326')

g.to_csv('Missing/DenverMissing.csv')
g.to_file('Missing/DenverMissing.geojson', driver = 'GeoJSON')

parcel_file = gpd.read_file('parcel_geometries')
parcel_file.head()
den_parcels = parcel_file[parcel_file.geom_id.str.contains('DE')]

den_parcels = gpd.GeoDataFrame(den_parcels, geometry = 'geometry', crs = 'EPSG:32613')

den_parcels.to_file('Missing/DenverParcels.geojson', driver = 'GeoJSON')
den_parcels.plot()

len(gdf)
len(p_df)

len(full_den)





out_df = pd.read_csv('OutFilesIndiv/DE.csv')
len(out_df)
out_df.uid.nunique()
