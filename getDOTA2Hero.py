import requests
import urllib.request as urllib2
from bs4 import BeautifulSoup as bs
import re
import json
import sys


headers = {'User-Agent': 'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
session = requests.session()
session.headers.update(headers)

hero_url_dict = {}
corps_url_dict = {}


def getHeroPageHref(url):
    try:
        soup = bs(session.get(url).text, "html5lib")
        soup.prettify()
        for child in soup.find_all(attrs={"class": "heroPickerIconLink"}):
            pageUrl = child["href"]
            hero_url_dict.__setitem__(pageUrl, 1)
    except:
        pass


def get_hero_info(hero_url):
    try:
        soup = bs(session.get(hero_url).text, "html5lib")
        soup.prettify()
        soup_hero_card = soup.find(attrs={"class": "top_hero_card"})
        tmp_soup = soup_hero_card.find(name="p")
        hero_name = tmp_soup.find(name="span").get_text().replace("\n", "").replace("\t", "").strip()
        tmp_soup.span.decompose()
        hero_name_en = tmp_soup.get_text().replace("\n", "").replace("\t", "").strip()

        soup_hero_info_ul = soup.find(attrs={"class": "info_ul"})
        info_1=[]
        for child in soup_hero_info_ul.find_all(attrs={"class": "clearfix"}):
            info_1.append(child.get_text().replace("\n", "").replace("\t", "").strip())

        soup_hero_skill_box = soup.find(id="focus_dl").find(name="ul")
        info_skill = []
        for child in soup_hero_skill_box.find_all(name="li"):
            child.img.decompose()
            info_skill.append(child.get_text().replace("\n", "").replace("\t", "").strip())

        return "\t".join([hero_name, hero_name_en, '|'.join(info_1), '|'.join(info_skill)]) + "\n"
    except:
        return ""


startUrl = "http://www.dota2.com.cn/heroes/index.htm"
getHeroPageHref(startUrl)

dota2_hero_file = open('E:\\PyProjects\\Work\\spider\\dota2_hero.txt', 'w', encoding="utf-8")
for heroUrl in hero_url_dict.keys():
    dota2_hero_file.write(get_hero_info(heroUrl))
    dota2_hero_file.flush()
dota2_hero_file.close()
