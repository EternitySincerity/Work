import requests
import urllib.request as urllib2
from bs4 import BeautifulSoup as bs
import re
import json
import sys

teamDetailUrl = 'http://lpl.qq.com/web201612/data/LOL_MATCH2_TEAM_TEAM%teamId%_INFO.js'
gameTeamUrl = 'http://lpl.qq.com/web201612/data/LOL_MATCH2_GAME_GAME%gameId%_INFO.js'
gameUrl = "http://lpl.qq.com/web201612/data/LOL_MATCH2_GAME_LIST_BRIEF.js"
teamUrl = "http://lpl.qq.com/web201612/data/LOL_MATCH2_TEAM_LIST.js"
teamMember = "http://lpl.qq.com/web201612/data/LOL_MATCH2_TEAM_MEMBER_LIST.js"
string_file = ""


def html_to_return_str(url, type):
    html_text = requests.get(url).text
    if html_text is not None and len(html_text) > 0:
        if html_text.__contains__("={"):
            html_text = html_text.split("=")[1]
        if html_text.endswith("};"):
            html_text = html_text.split(";")[0]
        try:
            html_text = json.loads(html_text)["msg"]
        except:
            html_text = ""
        extract_string(type, html_text)


def extract_string(orient_string, object_string):
    global string_file
    if isinstance(object_string, dict):
        for key in object_string.keys():
            try:
                string_file = string_file + (orient_string + '\t' + key + '\t' + object_string[key] + '\n')
            except Exception:
                extract_string(orient_string + '\t' + key + '\t', object_string[key])
    elif isinstance(object_string, list):
        for i in range(0, len(object_string)):
            tmp_tmp_object = object_string[i]
            for key in tmp_tmp_object.keys():
                extract_string(orient_string + '\t' + key + '\t', tmp_tmp_object[key])
    elif object_string is not None and len(object_string) > 0:
        string_file = string_file + orient_string + "\t" + object_string + '\n'


html_to_return_str(gameUrl, "game")
html_to_return_str(teamUrl, "team")
html_to_return_str(teamMember, "member")

gameIdList = {}
teamIdList = {}
for i in string_file.split("\n"):
    if i.split("\t").__contains__("GameId") and i.split("\t").__contains__("sGameList"):
        gameIdList.__setitem__(str(i.split("\t")[-1]), str(i.split("\t")[-1]))
    if i.split("\t").__contains__("TeamId"):
        teamIdList.__setitem__(str(i.split("\t")[-1]), str(i.split("\t")[-1]))

for i in gameIdList.keys():
    gameTeamUrl_final = gameTeamUrl.replace("%gameId%", str(i))
    html_to_return_str(gameTeamUrl_final, "gameTeam")
for i in teamIdList.keys():
    teamDetailUrl_final = teamDetailUrl.replace("%teamId%", str(i))
    html_to_return_str(teamDetailUrl_final, "teamDetail")

soup = bs(urllib2.urlopen("http://lpl.qq.com/es/2017worlds/").read(), "html5lib")
soup.prettify()
for child in soup.find_all(attrs={"class": "m-commentator-wrapper swiper-wrapper"}):
    for sub_child in child.find_all(attrs={"class": "m-team-li"}):
        string_file = string_file + ('\t'.join(['commentator', 'name', sub_child.get_text().strip()]) + "\n")

file_lol = open('E:\\lol.txt', 'w', encoding="utf-8")
file_lol.write(string_file)
file_lol.flush()
file_lol.close()
