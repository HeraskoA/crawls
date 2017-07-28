import os
import zipfile
import pandas as pd
import csv

out = pd.read_csv("/data/work/virtualenvs/scrapy/crawls/result_regalpts.csv", sep=',')
catalog_numbers = list(out.catalog_number)
ids = list(out.ids)
catalog_ids = dict(zip(catalog_numbers, ids))

path = '/data/work/virtualenvs/scrapy/crawls/regalpts_download'
files = os.listdir(path)
'''
catalog = []
for file in files:
	if not zipfile.is_zipfile(path + '/' + file):
		catalog.append(file.replace('_', '/').replace('.zip', ''))

with open('bad1.csv', 'wb') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"')
    for item in catalog:
    	spamwriter.writerow([item])
'''
with open('regalpts_links.csv', 'wb') as csvfile:
	spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"')
	spamwriter.writerow(['id', 'catalog_number', 'cad'])
	for file in files:
		f=zipfile.ZipFile(path +'/' + file, 'r')
		filename = f.namelist()[0]
		print filename
		item = file.replace('_', '/').replace('.zip', '').strip()
		link = 'https://mro-host.herokuapp.com/file_download/?name=regalpts_' + filename
		spamwriter.writerow([catalog_ids[item], item, link])
		f.extractall('/data/work/virtualenvs/scrapy/crawls/regalpts_unzip')
		f.close()