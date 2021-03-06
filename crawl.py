import requests
import pandas as pd
import xmltodict
from tqdm import tqdm
from pandas import ExcelWriter

def get_status(requestUrl):
     r = requests.get(requestUrl)
     return r.status_code

url = ""
res = requests.get(url)
raw = xmltodict.parse(res.text)

data = [[r["loc"]] for r in raw["urlset"]["url"]]
print("Number of sitemaps:", len(data))

df = pd.DataFrame(data, columns=["loc"])
df['status'] = 0

with tqdm(total=len(data)) as pbar:
     for index, row in df.iterrows():
          df.set_value(index,'status', get_status(row['loc']))
          #print(row['loc'] + " --------- " + str(df.get_value(index, 'status')))
          pbar.update(1)
          pbar.set_description("Processing sitemap")

writer = pd.ExcelWriter('results.xlsx', engine='xlsxwriter',options={'strings_to_urls': False})
df.to_excel(writer, sheet_name='Sheet1', index=False)
writer.save()