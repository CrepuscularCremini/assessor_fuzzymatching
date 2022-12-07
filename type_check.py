import pandas as pd
import geopandas as gpd

df = gpd.read_file(r'RHNA_Local_2020\08001\Adams_County2020\Parcels.shp')

tdf = df.sample(50)
tdf.to_excel('TestParcels/test.xlsx')
