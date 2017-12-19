import urllib.request as urllib2
from bs4 import BeautifulSoup as bs
import re

startUrl = "http://yy.8fkd.com"


def getActorList(url):
    retList = []
    try:
        soup = bs(urllib2.urlopen(url).read(), "html5lib")
        soup.prettify()
        soup = soup.find(attrs={"class": "divRect"})
        for child in soup.find(attrs={"class": "divBody"}).find_all(attrs={"class": "divItem"}):
            link = str(child.find(attrs={"class": "aFace"}).get("href"))
            img = str(child.find(attrs={"class": "aFace"}).find("img").get("src"))
            actorName = str(child.find(attrs={"class": "aName"}).contents[0])
            briefDesc = str(child.find(attrs={"class": "liRight"}).contents[0])
            if not re.match(link, r'^http'):
                link = startUrl + link
            retList.append([link, actorName, img, briefDesc])
        return retList
    except:
        pass


def getActor(url):
    retList = []
    try:
        actorInfo = []
        soup = bs(urllib2.urlopen(url).read(), "html5lib")
        soup.prettify()
        soup_info = soup.find(id="divActorInfo")
        for child in soup_info.find(re.compile("^ul$")).find_all("li"):
            if not child.has_attr("style"):
                actorInfo.append(child.contents[0].replace('\n', ''))
        breif_desc = soup.find(attrs={"class": "divIntroduce"}).find(attrs={"class": "text"}).get_text().replace('\n',
                                                                                                                 '')
        actorInfo.append(breif_desc)

        retList.append([url, '\t'.join(actorInfo)])
        return retList
    except:
        pass


def getopuslist(url, opusType):
    retList = []
    try:
        opusList = []
        if opusType == 1:
            url_tar = url + "/DianShiJu"
        elif opusType == 2:
            url_tar = url + "/DianYing"
        elif opusType == 3:
            url_tar = url + "/JueSe"

        soup = bs(urllib2.urlopen(url_tar).read(), "html5lib")
        soup.prettify()
        soup_info = soup.find(attrs={"class": "divLeftRect"}).find(attrs={"class": "divBody"})

        # print(soup_info)
        if opusType == 1 or opusType == 2:
            for child in soup_info.find_all(attrs={"class": "divItem"}):
                try:
                    opusList.append('\t'.join([child.find(attrs={"class": "li1"}).get_text(),
                                               child.find(attrs={"class": "li3"}).get_text(),
                                               child.find(attrs={"class": "li4"}).get_text()]))
                except:
                    pass
            print(opusList)
        elif opusType == 3:
            try:
                opusList.append([soup_info.get_text().replace('\n', '')])
            except:
                pass
            print(opusList)

        retList.append(['\t'.join(opusList)])
        return retList
    except:
        pass


for pageindex in range(1, 3):
    breifInfo = getActorList("http://yy.8fkd.com/YanYuanKu/Search.aspx?page=" + str(pageindex))
    file_object = open('E:\\PyProjects\\Work\\spider\\breifUrl.txt', 'a', encoding="utf-8")
    file_actor = open('E:\\PyProjects\\Work\\spider\\Actor.txt', 'a', encoding="utf-8")
    for breif in breifInfo:
        file_object.write('\t'.join([breif[0], breif[1], breif[2], breif[3], '\n']))
        actor = getActor(breif[0])
        print(actor, getopuslist(breif[0], 2))
        # 1-电视剧 2-电影 3-角色
        # drama = [getopuslist(breif[0],1),getopuslist(breif[0],2),getopuslist(breif[0],3)]
        # if not (actor is None and len(actor) > 0):
        #     file_actor.write('\t'.join(actor[0]).join(''.join(getopuslist(breif[0], 1))) + '\n')
        #     file_actor.write('\t'.join(actor[0]).join(''.join(getopuslist(breif[0], 2))) + '\n')
        #     file_actor.write('\t'.join(actor[0]).join(''.join(getopuslist(breif[0], 3))) + '\n')
        break
    file_object.close()
    file_actor.close()
