import re
import pandas as pd
import csv


f = open('DOC#2052637.txt', 'r')
data = f.read()
f.close()

GP1 = 0.00
GP2 = 0.00
freight = 0.00
ExtPrice = 0.00
sold_items = 0

item_list = data.split('****************************************************************************************************************************************************')[:-1]

for item in item_list:
	item = item.split('Order #')[1]
	freight += float(re.findall(r'Freight :\s+([\d\.]+)\s+Handling', item)[0])
	ExtPriceList = re.findall(r'\s+[ -]\d+\.\d+\s+[ -]\d+\.\d+\s+[ -]\d+\.\d+\s+([ -]\d+\.\d+)\s+[ -]\d+\.\d+\s+[ -]\d+\.\d+\s', item)
	GP1List = re.findall(r'\s+[ -]\d+\.\d+\s+[ -]\d+\.\d+\s+[ -]\d+\.\d+\s+[ -]\d+\.\d+\s+([ -]\d+\.\d)+\s+[ -]\d+\.\d+\s', item)
	GP2List = re.findall(r'\s+[ -]\d+\.\d+\s+[ -]\d+\.\d+\s+[ -]\d+\.\d+\s+[ -]\d+\.\d+\s+[ -]\d+\.\d+\s+([ -]\d+\.\d)+\s', item)
	for item in ExtPriceList:
		ExtPrice += float(item)
	for item in GP1List:
		GP1 += float(item)
	for item in GP2List:
		GP2 += float(item)
	sold_items += len(ExtPriceList) 

GP2 = GP2/sold_items


order_count = len(item_list)

print [
	str(order_count), 
	str(sold_items), 
	str(freight), 
	str(ExtPrice), 
	str(GP1), 
	str(GP2)
	]


