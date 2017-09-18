import pandas as pd
import json


path = 'result_armani.csv'

countries = {
    'United States': 'USD',
    'France': 'EUR',
}

df = pd.read_csv(path)

items_count = len(df['name'])
out_json = {}
true_currency = True
regions = list(df.region)
currency = list(df.currency)
colors = len([color for color in list(df['color']) if str(color) != 'nan'])
sizes = len([size for size in list(df['size']) if str(size) != 'OneSize'])
descriptions = len([description for description in list(df['description']) if str(description) != 'nan'])
region_currency = dict(zip(regions, currency))
regions_list = set(df['region'])

for region in regions_list:
	out_json['number of items in ' + region.lower()] = len([reg for reg in regions if reg == region])

for region in regions:
	if region_currency[region] != countries[region]:
		error = False

out_json['part of colors'] = str(100*colors/items_count) + '%'
out_json['part of sizes'] = str(100*sizes/items_count) + '%'
out_json['part of descriptions'] = str(100*descriptions/items_count) +'%'
out_json['true currency'] = true_currency

content = json.dumps(out_json, sort_keys=True, indent=4)
f = open('result_test.json', 'w')
f.write(content)
f.close()