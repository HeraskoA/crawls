import os
path = '/data/work/virtualenvs/scrapy/crawls/regalpts_unzip'
files = os.listdir(path)

for file in files:
    os.rename(os.path.join(path, file), os.path.join(path, 'regalpts_' + os.path.splitext(os.path.basename(file))[0] +'.IGS'))

"""
1 compl
2 compl
3 compl
4 compl
5 compl
6 compl
7 compl
8 compl
9 compl
"""