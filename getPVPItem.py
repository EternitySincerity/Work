import requests
import urllib.request as urllib2
from bs4 import BeautifulSoup as bs
import re
import json
import sys


headers = {'User-Agent': 'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
session = requests.session()
session.headers.update(headers)


pvp_item_file = open('E:\\PyProjects\\Work\\spider\\pvp_item.txt', 'w', encoding="utf-8")
startUrl = "http://pvp.qq.com/web201605/js/item.json"
item_list = json.loads(session.get(startUrl).text)
for item in item_list:
    item_txt = []
    for key in item.keys():
        item_txt.append(str(item[key]).replace("\n", "|").replace("	", "|").replace("<br>", "|").replace("<p>", "").replace("</p>", "").strip())
    pvp_item_file.write('\t'.join(item_txt) + '\n')

pvp_item_file.close()

pvp_talent_file = open('E:\\PyProjects\\Work\\spider\\pvp_talent.txt', 'w', encoding="utf-8")
startUrl = "http://pvp.qq.com/web201605/js/summoner.json"
item_list = json.loads(session.get(startUrl).text)
for item in item_list:
    item_txt = []
    for key in item.keys():
        item_txt.append(str(item[key]).replace("\n", "|").replace("	", "|").replace("<br>", "|").replace("<p>", "").replace("</p>", "").strip())
    pvp_talent_file.write('\t'.join(item_txt) + '\n')

pvp_talent_file.close()
