import pandas as pd
import os
import numpy as np

os.chdir('CensusGeography/')

d20 = pd.read_csv('GeomID_2020.csv')
d19 = pd.read_csv('GeomID_2019.csv')

keep_cols = ['geom_id', 'GEOID']
d20 = d20[keep_cols].copy()
d20['GEOID'] = d20.GEOID.apply(lambda x: str(int(x)).zfill(12) if pd.notnull(x) else np.nan)
d20.rename(columns = {'GEOID' : 'bg_id_2020'}, inplace = True)
d20['tract_id_2020'] = d20.bg_id_2020.str[:-1]

d19 = d19[keep_cols].copy()
d19['GEOID'] = d19.GEOID.apply(lambda x: str(int(x)).zfill(12) if pd.notnull(x) else np.nan)
d19.rename(columns = {'GEOID' : 'bg_id_2010'}, inplace = True)
d19['tract_id_2010'] = d19.bg_id_2010.str[:-1]

df = d20.merge(d19, on = 'geom_id')
df.to_csv('parcel_to_census.csv')
