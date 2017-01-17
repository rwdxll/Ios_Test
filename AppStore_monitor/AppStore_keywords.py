#!/usr/bin/env python
#-*-coding:utf-8 -*-

import os
import sys
import re
import time
import json
import requests

import html5lib
from bs4 import BeautifulSoup

appName = u"旧爱闲置-闲置物品交易购物平台"

ios_app_keywords = ["旧爱","二手","闲置","闲鱼","咸鱼网","转转","少铺",
				"空空狐","心上","花粉儿","百姓","赶集网","xianyu","爱丁猫","天猫",
				"淘宝","手机版","taobao58","同城app","数码宝贝","鱼塘","秒赚","寺库",
				"胖虎","打折扣","买卖","衣服","奢侈品","奢家","代购","母婴","挣钱",
				"包优购","支付宝","返利网","心上"]

#download search page
def search_pages(keywords):
	headers = {
		"Connection":"keep-alive",
		"Content-Type":"text/html",
		"Cache-Control":"max-age=0",
		"User-Agent":"Mozilla/5.0 (Windows NT 10.0;WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
		"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
		"Accept-Encoding":"gzip,deflate,sdch,br",
		"Accept-Language":"zh-CN,zh;q=0.8"
		}

	responsePage = requests.get('https://aso100.com/search?country=cn&search={0}'.format(keywords),headers=headers)
	return responsePage.content
	

#获取Appstore排名List
def get_appstore_ranking_results(page):

	pageTitle = u'搜索结果'

	soup = BeautifulSoup(page,'html.parser')
	if pageTitle not in soup.title:
		print(soup.title.encode("gbk"))

	appstore_results = [ranking for applist in soup.find_all(class_="app-list") 
							for rankList in applist.find_all('h4',class_="media-heading") 
							for ranking in rankList.find('a')]
	return appstore_results

keyword_ranking = [r for keyword in ios_app_keywords for r in get_appstore_ranking_results(search_pages(keyword)) if appName in r ]

print json.dumps(dict(zip(ios_app_keywords,keyword_ranking)), encoding="UTF-8", ensure_ascii=False)
