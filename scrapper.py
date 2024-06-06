import os
from io import StringIO
import pandas as pd
import requests as req
from settings import BASE_DIR

"""
Parses a table on the website (url) and receives a short translation
for each cryptocurrency.
P.S. Of course, not all cryptocurrencies are presented in the table
this was created to simplify life if a person does not know how to
abbreviate cryptocurrency.
"""

url = 'https://www.ifcmarkets.com/en/cryptocurrency-abbreviations'

res_path = os.path.join(BASE_DIR, 'app', 'symbols.txt')

response = req.get(url)

html = StringIO(str(response.text))
table = pd.read_html(html)
records = table[0].values.tolist()

data = {}

for record in records:
    data[record[1]] = [record[0].upper(), record[2].upper()]

with open(res_path, 'w', encoding='utf8') as f:
    print(data, file=f)
