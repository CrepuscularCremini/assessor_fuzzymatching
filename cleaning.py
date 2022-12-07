import pandas as pd
import os

os.chdir('RHNA_Local_2020/')

df = pd.read_csv('BasicLightBox/basic_light_box_parcels.csv')

rows = df.use_code_muni_desc.str.lower().dropna().unique().tolist()
rows.sort()

ag = ['ag ', 'agri', 'barn', 'farm', 'grain', 'grazing', 'greenhouse', 'horse', 'lumber', 'shed', 'ac']
airport = ['airport', 'hangar']
civic = ['federal', 'fed ', 'fire ', 'fire/', 'government', 'hospitality', 'jail', 'library', 'medical', 'hospital', 'police', 'post office', 'school',\
        'water', 'admin', 'college', 'elem/second', 'mail', 'meeting', 'vet']
exempt = ['ex ', 'exempt', 'county', 'state', 'religous', 'worship', 'church']
industrial = ['auto', 'car ', 'carwash', 'factory', 'garage service', 'garage storage', 'industrial', 'indust', 'warehouse', 'computer ', 'data ', 'equipment',
        'food process', 'gas', 'manufacturing', 'material shalter', 'storage', 'meat packing', 'kennel']
mining = ['mineral', 'earth/stone', 'mine', 'service']
office = ['office']
open = ['camp', 'park', 'forest', 'golf', 'open', 'recreation', 'club']
residential = ['apartment', 'apt', 'bed ', 'condo', 'residential', 'dorm', 'double wide', 'plex', 'shelter', 'frat', 'homes', 'hotel', 'shelter', 'lodges',\
                'manufactured', 'manufctrd', 'res', 'mobile home', 'modular', 'motel', 'multi-story', 'multi-unit', 'living', '-rise', 'senior', 'sfr', 'story',\
                'single fam', 'split-level', 'house', 'townhouse', 'unit', 'boarding', 'bi-level', 'home', 'lodg', 'quonset', 'retirement care', 'single wide',\
                'triple wide', 'studio', 'cabin']
retail = ['bank', 'banq', 'bar/', 'bowling', 'department', 'dept', 'fast ', 'financial', 'general', 'commercial', 'retail', 'shopping', 'restaurant', 'theater',\
            'barber', 'brewery', 'day care', 'daycare', 'convenience', 'store', 'dry cleaning', 'fitness', 'comm', 'mall', 'market', 'comm', 'shop', 'theatre']
vacant = ['vacant', 'vcnt', 'vac']
parking = ['parking']

class_dictionary = {\
                    'vacant' : vacant,
                    'exempt' : exempt,
                    'parking' : parking,
                    'ag' : ag,
                    'airport' : airport,
                    'civic' : civic,
                    'residential' : residential,
                    'open' : open,
                    'retail' : retail,
                    'industrial' : industrial,
                    'office' : office,
                    'mining' : mining
            }

from collections import OrderedDict
rev = OrderedDict(reversed(list(class_dictionary.items())))

cd = pd.DataFrame.from_dict({'use_code_muni_desc' : rows})

for idx, val in cd.iterrows():
    for classification, vals in rev.items():
        for comp in vals:
            if comp in val['use_code_muni_desc']:
                cd.loc[idx, 'use_code_class'] = classification

cd.to_csv('muni_desc.csv', index = False)

print('Non Coded: {0}'.format(cd.use_code_class.isna().sum()))
