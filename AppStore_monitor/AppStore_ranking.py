#!/usr/bin/env python
#-*-coding:utf-8 -*-

#base on Python2.7
#2017-02-13 update

import os
import sys
import re
import time
import json
import random
import requests
from requests import Session
from bs4 import BeautifulSoup
from pprint import pprint

APP_NAME = u"旧爱闲置-闲置物品交易购物平台"

ios_app_keywords = ["旧爱","二手","闲置","奢侈品","闲鱼","转转","少铺","空空狐","心上","花粉儿","咸鱼网",
    "百姓","赶集网","xianyu","爱丁猫","天猫","淘宝","手机版","taobao58","同城app","数码宝贝","鱼塘",
    "秒赚","寺库","胖虎","打折扣","买卖","衣服","奢家","代购","母婴","挣钱","包优购","支付宝","返利网"]

all_result,assign_result = {}.fromkeys(ios_app_keywords),{}.fromkeys(ios_app_keywords)

headers = {
    "Connection":"keep-alive",
    "Content-Type":"text/html",
    "Cache-Control":"no-cache",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0;WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding":"gzip,deflate,sdch,br",
    "Accept-Language":"zh-CN,zh;q=0.8"
    }

#download search page
def get_search_pages(keywords):
    expected_title = u'搜索结果'
    serach_result = []
    try:
        while 1:
            # fix https ssl questions
            requests.packages.urllib3.disable_warnings()

            session = requests.Session()
            session.headers = headers
            response = session.get('https://aso100.com/search?country=cn&search={0}'.
                format(keywords),verify=False)

            # print("--------------------------\n")
            # print(session.cookies.get_dict())
            # print(session.headers)
            #打印titile
            soup = BeautifulSoup(response.content,'html.parser')
            soup_title= soup.title.prettify()
            response_title = soup_title.replace("<title>","").replace("</title>","").strip()

            if expected_title in response_title:
                print("\n {0}..........................ok \n".format(response_title.encode("gbk")))
                break
            elif response.status_code != 200:
                response.cookies.clear()
                print("-> {0}: Page error........{1}".format(keywords,response.status_code))
            else:
                print(response_title)
                #session.headers.update({"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko"})
                time.sleep(10)
    except requests.URLRequired:
        print(" -> A valid URL is required to make a reques.\n")
    except requests.ConnectionError:
        print(" -> Network connection error.\n")
        sys.exit()
    except requests.HTTPError:
        print(" -> An HTTP error occurred.\n")
    except (requests.Timeout,requests.ConnectTimeout) as e:
        print(" -> The request or trying to connect servertimed out.\n")

    try:
        serach_result = [ranking for applist in soup.find_all(class_="app-list") 
                    for rankList in applist.find_all('h4',class_="media-heading") 
                    for ranking in rankList.find('a')]
    except Exception as e:
        print(e)
    return serach_result

for keyword in ios_app_keywords:
    get_result = get_search_pages(keyword)
    all_result[keyword] = get_result
    for rt in get_result:
        if APP_NAME in rt:
            patter = re.compile("[1-9]+")
            assign_result[keyword] = ''.join(re.findall(patter,rt))

#筛选出包括特定包名的搜索结果
print("\n -> AppStore: Search Result Before 20..................\n")
print(json.dumps(all_result, encoding="UTF-8", ensure_ascii=False,indent=4))
print("\n -> AppStore: App ranking.............................\n")
print(json.dumps(assign_result, encoding="UTF-8", ensure_ascii=False,indent=4))
