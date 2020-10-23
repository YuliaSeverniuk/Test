import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

main_url = "https://www.the-village.com.ua/"

main_html = requests.get(main_url)
result = pd.DataFrame()


def get_content(html):
    soup = BeautifulSoup(html, "html.parser")
    return soup


def parse_news(child_url):
    res = pd.DataFrame()
    child_html = requests.get(main_url+child_url)
    category = get_content(child_html.text).find_all('a', href=child_url)
    header = get_content(child_html.text).find_all('h3', {'class': 'post-title'})
    date = get_content(child_html.text).find_all('span', {'class': 'post-date'})
    time = get_content(child_html.text).find_all('span', {'class': 'post-time'})

    for c in category:
        news_category = c.get_text()
        res = res.append(pd.DataFrame([[news_category]], columns=["news_category"]), ignore_index=True)

    for (h, d, t) in zip(header, date, time):
        news_header = h.get_text()
        news_date = d.get_text()
        news_time = t.get_text()
        res = res.append(pd.DataFrame([[news_header, news_date, news_time]],
                                      columns=["news_header", "news_date", "news_time"]), ignore_index=True)

    return res


links = get_content(main_html.text).find_all('div', {'class': 'controls'})
for link in links:
    urls = re.findall('href="(.*?)">', str(link))
    for url in urls:
        res = parse_news(url)
        result = result.append(res, ignore_index=True)

result.to_csv("result.csv")


