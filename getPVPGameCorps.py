import requests
import urllib.request as urllib2
from bs4 import BeautifulSoup as bs
import re
import simplejson as json
import sys

headers = {'User-Agent': 'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
session = requests.session()
session.headers.update(headers)

pvp_game_corps_file = open('E:\\PyProjects\\Work\\spider\\pvp_game_corps.txt', 'w', encoding="utf-8")
startUrl = "http://pvp.qq.com/match/kpl/js/play-info-1709.js"
str_data = session.get(startUrl).text.split("=")[1].replace("'", "\"").replace("\r\n", "").replace("\t", "").strip()
# print(session.get(startUrl).text.split("=")[1])
str_data = str_data.replace(" :","\":").replace("\",", "\",\"").replace("\"\"", "\"").replace("{","{\"").replace("],","],\"")
str_data = str_data.replace("\"[\"","[\"")
item_list = json.loads(str_data)
for item in item_list:
    item_txt = []
    for key in item.keys():
        item_txt.append(str(item[key]).replace("\n", "|").replace("	", "|").replace("<br>", "|").replace("<p>", "").replace("</p>", "").strip())
    pvp_game_corps_file.write(str(item_txt) + "\n")
    pvp_game_corps_file.flush()

# kpl_jieshuo_cbox
pvp_game_corps_file.close()