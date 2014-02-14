# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import re as re

# <codecell>

# have to store the data 
df = pd.DataFrame(columns={'Symbol', 'Fund Name', 'Category', 'Expense Ratio'})

# <codecell>

# mutual fund ticker symbol
symbol_list = ['VGTSX']

# <codecell>

# url creation
options_url = 'http://finance.yahoo.com/q?s=' + symbol_list[0]
options_page = urlopen(options_url)

# <codecell>

# create the soup
soup = BeautifulSoup(options_page)

# <codecell>

# parse out the title
for title in soup.findAll("div", {"class": "title"}):
    fund_name = title.text

# <codecell>

# parse out the fund type
for cell in soup.findAll("th", {"scope": "row"}):
    if 'Category' in cell.text: 
        category = cell.nextSibling.text

# <codecell>

# find the annual expense ratio, remove the % and convert to decimal
for cell in soup.findAll("th", {"scope": "row"}):
    if 'Annual' in cell.text:
       expense = float(re.sub(r'\%', ' ', cell.nextSibling.text))

# <codecell>

# add it into the DataFrame
df = df.append({'Symbol': symbol_list[0], 'Fund Name': fund_name, 'Category': category, 'Expense Ratio': expense},ignore_index = True)

# <codecell>

df

