# scr/main.py

import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
from fake_useragent import UserAgent
from helpers.utils import save_to_sqlite3


ua = UserAgent()
useragent = ua.random

session = requests.Session()
session.headers["User-Agent"] = useragent


url = "https://www.imdb.com/chart/top/?ref_=nv_mv_250"

page = session.get(url)
soup = bs(page.content, 'html.parser')
movies = soup.select('li.DLYcv.cli-parent')


results = []
for movie in movies:
    result = {
        'title': movie.select_one('h3.ipc-title__text').text,
        'year': movie.select_one('span.sc-5bc66c50-6.OOdsw.cli-title-metadata-item').text

    }
    results.append(result)

data = pd.DataFrame(results)
print(data.info())
print('*'*100)
data.to_csv('../data/results.csv', index=False)
save_to_sqlite3(data)
