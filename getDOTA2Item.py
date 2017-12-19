import requests
import urllib.request as urllib2
from bs4 import BeautifulSoup as bs
import re
import json
import sys


headers = {'User-Agent': 'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
session = requests.session()
session.headers.update(headers)


dota2_item_file = open('E:\\PyProjects\\Work\\spider\\dota2_item.txt', 'w', encoding="utf-8")
startUrl = "http://www.dota2.com.cn/js/items.js"
html_text = requests.get(startUrl).text
pattern = re.compile('itemsJson=([^(\};)]*)\};', re.S | re.M)

if html_text is not None and len(html_text) > 0:
    html_text = re.search(pattern, html_text).group()

    if html_text.__contains__("={"):
        html_text = '{' + html_text.split("={")[1]
    if html_text.endswith("};"):
        html_text = html_text.split("};")[0].replace("\"", "") + '}'

    for item in html_text.split("['"):
        if item.__contains__("','"):
            dota2_item_file.write(item.split("','")[0] + '\n')


#
# for heroUrl in hero_url_dict.keys():
#     dota2_item_file.write(get_hero_info(heroUrl))
#     dota2_item_file.flush()
dota2_item_file.close()
