import re
import pandas as pd
import csv

out = pd.read_csv("/data/work/virtualenvs/scrapy/crawls/skf_seals_download.csv", sep=',')
catalog_numbers = list(out.catalog_number)
ids = list(out.ids)
descr = list(out.file_name)
catalog_ids = dict(zip(catalog_numbers, ids))
catalog_descr = dict(zip(catalog_numbers, descr))

with open('skf_seals_download_without_nan_items.csv', 'wb') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"')
    spamwriter.writerow(['id', 'catalog_number', 'file_name'])
    for item in catalog_numbers:
    	if str(catalog_descr[item]) != 'nan':
    		spamwriter.writerow([catalog_ids[item], item])

