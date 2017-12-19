import requests
import urllib.request as urllib2
from bs4 import BeautifulSoup as bs
import re
import json
import sys


headers = {'User-Agent': 'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
session = requests.session()
session.headers.update(headers)

member_url_dict = {}
corps_url_dict = {}

def getMemberPageHref(url):
    try:
        soup = bs(session.get(url).text, "html5lib")
        soup.prettify()
        soup_body = soup.find(attrs={"class": "plate playercont"})
        for child in soup_body.find_all(name="li"):
            pageUrl = child.a["href"]
            member_url_dict.__setitem__(pageUrl, url)

        soup_next_url = soup.find(attrs={"class": "pages"}).find(attrs={"class": "next"})
        if soup_next_url is not None:
            next_url = domainUrl + soup_next_url.a["href"]
            getMemberPageHref(next_url)
        else:
            # print(member_url_dict)
            pass
    except:
        pass


def get_member_info(member_url):
    try:
        soup = bs(session.get(member_url).text, "html5lib")
        soup.prettify()
        soup = soup.find(attrs={"class": "player-info"})

        player_name = soup.find(attrs={"class": "player-name"}).get_text()

        player_info_soup = soup.find_all(name="em")
        if len(player_info_soup) == 4:
            player_real_name = player_info_soup[0].get_text()
            player_corps = player_info_soup[1].get_text()
            player_game_place = player_info_soup[3].get_text()
        elif len(player_info_soup) == 3:
            player_real_name = ""
            player_corps = player_info_soup[0].get_text()
            player_game_place = player_info_soup[2].get_text()
        else:
            player_real_name = ""
            player_corps = player_info_soup[0].get_text()
            player_game_place = ""

        about_game_soup = soup.find(attrs={"class": "about-games"})
        player_in_game = about_game_soup.find(attrs={"class": "mr_35"}).get_text()
        try:
            corps_url_dict.__setitem__(about_game_soup.find(attrs={"class": "follow about-team"}).a["href"], player_in_game)
        except:
            pass

        return "\t".join([player_name, player_in_game, player_real_name, player_corps, player_game_place]) + "\n"
    except:
        return ""


def get_corps_info(corps_url):
    try:
        soup = bs(session.get(corps_url).text, "html5lib")
        soup.prettify()
        soup = soup.find(attrs={"class": "player-info"})

        corps_name = soup.find(attrs={"class": "player-name"}).get_text()

        corps_info_soup = soup.find_all(name="em")
        corps_full_name = corps_info_soup[0].get_text()
        corps_create_time = corps_info_soup[2].get_text()

        return "\t".join([corps_name, corps_full_name, corps_create_time]) + "\n"
    except:
        return ""


domainUrl = "http://gg.kaifu.com"
startUrl = "http://gg.kaifu.com/xs/1.html"
getMemberPageHref(startUrl)

game_member_file = open('E:\\PyProjects\\Work\\spider\\game_member.txt', 'w', encoding="utf-8")
for memberUrl in member_url_dict.keys():
    game_member_file.write(get_member_info(memberUrl))
game_member_file.flush()
game_member_file.close()

game_corps_file = open('E:\\PyProjects\\Work\\spider\\game_corps.txt', 'w', encoding="utf-8")
for corps_url in corps_url_dict.keys():
    game_corps_file.write(get_corps_info(corps_url))
game_corps_file.flush()
game_corps_file.close()
