import requests
import zipfile
import os

def tigerline_downloader(year, level, geography, out_folder, unzip = False):

    zip_filepath = "{0}/{1}_{2}_{3}.zip".format(out_folder, year, geography, level)
    out_dir = "{0}/{1}_{2}_{3}".format(out_folder, year, geography, level)


    base_url = "https://www2.census.gov/geo/tiger/TIGER{0}/{1}/tl_{0}_{2}_{3}.zip"
    form_url = base_url.format(year, level.upper(), geography, level)

    r = requests.get(form_url, stream = True)
    with open(zip_filepath, 'wb') as file:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                file.write(chunk)

    if unzip == True:
        with zipfile.ZipFile(zip_filepath, 'r') as zip_ref:
            zip_ref.extractall(out_dir)

census_geography = {'Tract' : 'tract',
                    'Block Group' : 'bg'}

year = '2019'
level = 'tract'
geography = '08'
out_folder = '.'

tigerline_downloader(year, level, geography, out_folder, unzip = True)
