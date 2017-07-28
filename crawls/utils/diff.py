import re
import pandas as pd
import csv

out = pd.read_csv("/data/work/virtualenvs/scrapy/crawls/regalpts.csv", sep=',')
catalog_numbers = list(out.catalog_number)
ids = list(out.id)
catalog_ids = dict(zip(catalog_numbers, ids))
out1 = pd.read_csv("/data/work/virtualenvs/scrapy/crawls/result_regalpts.csv", sep=',')
catalog_numbers1 = list(out1.catalog_number)

ca_num = [str(item).strip() for item in catalog_numbers]



with open('diff_regalpts', 'wb') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"')
    diff = [item for item in ca_num if item not in catalog_numbers1]
    spamwriter.writerow(['id', 'catalog_number'])
    for item in diff:
    	if str(item) != 'nan': 
    		spamwriter.writerow([catalog_ids[item], item])

