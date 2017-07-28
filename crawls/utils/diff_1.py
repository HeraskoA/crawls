import re
import pandas as pd
import csv

out = pd.read_csv("/data/work/virtualenvs/scrapy/crawls/result_regalpts.csv", sep=',')
catalog_numbers = list(out.catalog_number)
ids = list(out.ids)
descr = list(out.cad)
catalog_ids = dict(zip(catalog_numbers, ids))
catalog_descr = dict(zip(catalog_numbers, descr))

diff = [item for item in catalog_numbers if str(catalog_descr[item]) == 'nan']

with open('regalpts_next_part.csv', 'wb') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"')
    spamwriter.writerow(['id', 'catalog_number'])
    for item in diff:
    	spamwriter.writerow([catalog_ids[item], item])

