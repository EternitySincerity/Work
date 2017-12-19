import requests
import urllib.request as urllib2
from bs4 import BeautifulSoup as bs
import re
import json
import sys


headers = {'User-Agent': 'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
session = requests.session()
session.headers.update(headers)

pvp_hero_file = open('E:\\PyProjects\\Work\\spider\\pvp_hero.txt', 'w', encoding="utf-8")
pvp_hero_skill_file = open('E:\\PyProjects\\Work\\spider\\pvp_hero_skill.txt', 'w', encoding="utf-8")
startUrl = "http://pvp.qq.com/web201605/js/herolist.json"
hero_list = json.loads(session.get(startUrl).text)
for hero in hero_list:
    hero_txt = []
    for key in hero.keys():
        hero_txt.append(str(hero[key]))
    soup = bs(session.get("http://pvp.qq.com/web201605/herodetail/" + hero_txt[0] + ".shtml").text.encode("ISO-8859-1"), "html5lib")
    soup.prettify()
    soup_hero_skill_box = soup.find(attrs={"class": "skill-show"})
    info_skill = []
    for child in soup_hero_skill_box.find_all(attrs={"class": "skill-name"}):
        info_skill.append(child.b.get_text().replace("\n", "").replace("\t", "").strip())

    pvp_hero_skill_file.write(hero_txt[0] + '\t' + '\t'.join(info_skill) + '\n')
    pvp_hero_file.write('\t'.join(hero_txt) + '\n')

pvp_hero_file.close()
pvp_hero_skill_file.close()
