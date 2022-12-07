import pandas as pd
import geopandas as gpd
import os
import numpy as np
import matplotlib.pyplot as plt

os.chdir('RHNA_Local_2020/')

lb = pd.read_csv('BasicLightBox/basic_light_box_parcels.csv')
mp = pd.read_csv('muni_desc_final.csv')

lb.use_code_muni_desc = lb.use_code_muni_desc.str.upper()
mp.use_code_muni_desc = mp.use_code_muni_desc.str.upper()

df = lb.merge(mp, on = 'use_code_muni_desc', how = 'left')

gdf = gpd.read_file('unique_parcel_geometries/unique_parcel_geometries.shp')

gdf['calc_acre'] = gdf.geometry.area * 2.471052e-4

fdf = gdf.merge(df, on = 'geom_id', how = 'right')
fdf.drop(columns = 'Unnamed: 0', inplace = True)

plus_minus = 0.15
def acre_comp(r):
    if (1-plus_minus) * r.assr_acreage <= r.calc_acre <= (1 + plus_minus) * r.assr_acreage:
        return 'match'
    elif pd.isna(r.assr_acreage):
        return 'no assr'
    else:
        return 'no match'

fdf['acre_match'] = fdf.apply(acre_comp, axis = 1)
fdf.acre_match.value_counts() / len(fdf)

key_cols = ['yr_blt', 'building_sqft', 'val_mrkt_land', 'val_mrkt_imprv']
for col in key_cols:
    cutoff = .05
    c1, c2 = fdf[col].quantile([0,1 - cutoff]).values
    vals = fdf[(fdf[col] <= c2) & (fdf[col] >= c1)][col].values

    fig, axs = plt.subplots(1,2)
    fig.suptitle(col)
    axs[0].boxplot(vals)
    axs[1].hist(vals, edgecolor = 'k')
    fig.savefig('cleaning/{0}.png'.format(col), facecolor = 'white', transparent = False)

'''
building_sqft (< 50)    92
    1   77
    9   1
    25  13
    48  1
val_mrkt_land (< 50)    933
val_mrkt_imprv (< 50)   72
'''

# len(fdf.query('building_sqft < 50'))
# len(fdf.query('val_mrkt_land < 50'))
# len(fdf.query('val_mrkt_imprv < 50'))

res = fdf.query('use_code_class == "residential"')

rg = res.groupby(['use_code_spec', 'yr_blt']).geom_id.nunique().reset_index()

cols = {'condo' : 'pink',
        'manufactured home' : 'purple',
        'multifamily' : 'darkblue',
        'other mmh' : 'darkgreen',
        'plex (du-, tri-, multi-)' : 'green',
        'sfh' : 'red',
        'townhouse' : 'blue'}

fig, ax = plt.subplots()
for col in cols.keys():
    comp = rg.query('use_code_spec == @col')
    color = cols[col]
    ax.plot(rg.yr_blt, rg.geom_id, color = color, label = col)
plt.legend()

sfh = fdf.query('use_code_spec == "sfh"')

for col in key_cols:
    cutoff = .02
    c1, c2 = sfh[col].quantile([0,1 - cutoff]).values
    vals = sfh[(sfh[col] <= c2) & (sfh[col] >= c1)][col].values

    fig, axs = plt.subplots(1,2)
    fig.suptitle('sfh ' + col)
    axs[0].boxplot(vals)
    axs[1].hist(vals, edgecolor = 'k')
    fig.savefig('sfh/{0}.png'.format(col), facecolor = 'white', transparent = False)


for col_val in ['building_sqft', 'val_mrkt_land', 'val_mrkt_imprv']:
    # col_val = 'building_sqft'

    fig, ax = plt.subplots()
    fig.suptitle('sfh scatter: year built v. {0}'.format(col_val))
    plt.scatter(x = sfh.yr_blt, y = sfh[col_val], s = 1)

    sf_yr_min = sfh.groupby('yr_blt')[col_val].min().reset_index()
    sf_yr_med = sfh.groupby('yr_blt')[col_val].median().reset_index()
    sf_yr_mean = sfh.groupby('yr_blt')[col_val].mean().reset_index()
    sf_yr_max = sfh.groupby('yr_blt')[col_val].max().reset_index()

    fig, ax = plt.subplots()
    fig.suptitle('sfh: year built v. {0}'.format(col_val))
    ax.scatter(x = sf_yr_min.yr_blt, y = sf_yr_min[col_val], color = 'blue', label = 'min')
    ax.scatter(x = sf_yr_med.yr_blt, y = sf_yr_med[col_val], color = 'green', label = 'median')
    ax.scatter(x = sf_yr_mean.yr_blt, y = sf_yr_mean[col_val], color = 'red', label = 'mean')
    ax.legend()
    fig.savefig('sfh/scatter_yrblt_{0}.png'.format(col_val))

zon = gpd.read_file('../Analysis/Zoning/ResidentialZoningDensityDRCOGRegion_RHNA_7_10_22/p20/rhna.gdb', layer = 'allDRCOG_GenZone')
zon['gen_zon'] = zon.apply(lambda r: r.GenZone if pd.notnull(r.GenZone) else r.GenZoning, axis = 1)
zon = zon[['gid', 'local_zon', 'gen_zon', 'geometry']].copy()
zon = zon[['gen_zon', 'geometry']].copy()

zon.to_crs(epsg = 32613, inplace = True)

geom = gdf[['geom_id', 'geometry']].copy()

geom = gpd.GeoDataFrame(geom, geometry = geom.geometry.centroid, crs = geom.crs)

jdf = geom.sjoin(zon, how = 'left')

# jdf.query('gen_zon == ""').plot()

jdf['gen_zon'] = jdf.gen_zon.replace('', np.nan)
jdf.gen_zon.isna().sum()
len(jdf)

na_jdf = jdf.dropna(subset = 'gen_zon')
na_jdf.geom_id.nunique()
len(na_jdf)


# inter = gpd.overlay(zon, zon, 'intersection')

# i = inter.query('gen_zon_1 != gen_zon_2 and gen_zon_1 != "" and gen_zon_2 != ""')
# i.head()

# i_vals = i.gen_zon_1.unique().tolist() + i.gen_zon_2.unique().tolist()
# i_vals

naj = na_jdf.groupby('geom_id').first().reset_index()

naj.drop(columns = ['geometry', 'index_right'], inplace = True)

zdf = fdf.merge(naj, on = 'geom_id')

res_zones = ['Residential', 'Residential_Low', 'Residential_Med', 'Res_MultiFam', 'Residential_MedHigh', 'MobileHome', 'Residential_High', 'ResidentialPUD', 'Residential_Med_High', 'MultiFamRes']
zdf.use_code_spec = zdf.use_code_spec.fillna('')

zdf.query('gen_zon in @res_zones', inplace = True)

zcat = 'Residential_Low'


fig, ax = plt.subplots()
gz = zdf.groupby(['gen_zon', 'use_code_class']).geom_id.count().reset_index()
gz_comp = gz.query('gen_zon == @zcat')
plt.pie(gz_comp.geom_id)
fig.savefig('sfh_zoning/all_types.png')

fig, ax = plt.subplots()
gzs = zdf.groupby(['gen_zon', 'use_code_spec']).geom_id.count().reset_index()
gzs_comp = gzs.query('gen_zon == @zcat and use_code_spec != ""')
plt.pie(gzs_comp.geom_id, labels = gzs_comp.use_code_spec, explode = [.1] * len(gzs_comp))
fig.savefig('sfh_zoning/res_types.png')
