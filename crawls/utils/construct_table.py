import re
import pandas as pd
import csv


f = open('a.html', 'r')
table = f.read()
f.close()
table = re.sub(r'</tbody>(\n|\s)+</table>(\n|\s)+</div>(\n|\s)+<div class="col-xs-12 col-sm-4">(\n|\s)+<table class="table table-striped table-hover xtt-table-50 ">(\n|\s)+<tbody>', '', table)
'''
table = re.findall(r'<table class="table">((.|\n)+)</table>', table)[0][0]
table = '<table>' + table + '</table>'
'''
#table = re.sub(r'</tbody>(\n|\s)+</table>(\n|\s)+</div>(\n|\s)+<div class="col-xs-12 col-sm-4">(\n|\s)+<table class="table table-striped table-hover xtt-table-50 ">(\n|\s)+<tbody>', '', table)

#table = table.replace('<div class="row product-info-specs">', '').replace('<div class="col-xs-12 col-sm-6">', '').replace('</div>', '').strip()

f = open('a1.html', 'w')
f.write(table)
f.close()

