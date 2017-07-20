import re
import pandas as pd
import csv

out = pd.read_csv("/data/work/virtualenvs/scrapy/crawls/crawls/spiders/data/skf_seals.csv", sep=',')
catalog_numbers = list(out.catalog_number)
ids = list(out.id)
catalog_ids = dict(zip(catalog_numbers, ids))
out1 = pd.read_csv("/data/work/virtualenvs/scrapy/crawls/skf_seals_download.csv", sep=',')
catalog_numbers1 = list(out1.catalog_number)

ca_num = [str(item).strip() for item in catalog_numbers]



with open('diff_skf_seals.csv', 'wb') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"')
    diff = [item for item in ca_num if item not in catalog_numbers1]
    spamwriter.writerow(['id', 'catalog_number'])
    for item in diff:
    	if item != 'nan':
    		spamwriter.writerow([catalog_ids[item], item])

