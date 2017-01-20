#!/usr/bin/env python
#-*-coding:utf-8 -*-

import os
import sys
import re
import time
import json
import random
import requests
from requests import Session
from bs4 import BeautifulSoup

appName = u"旧爱闲置-闲置物品交易购物平台"

ios_app_keywords = [
	"旧爱","二手","闲置","奢侈品","闲鱼","转转","少铺","空空狐","心上","花粉儿","咸鱼网",
	"百姓","赶集网","xianyu","爱丁猫","天猫","淘宝","手机版","taobao58","同城app",
	"数码宝贝","鱼塘","秒赚","寺库","胖虎","打折扣","买卖","衣服","奢家",
	"代购","母婴","挣钱","包优购","支付宝","返利网","心上"]

headers = {
	"Connection":"keep-alive",
	"Content-Type":"text/html",
	"Cache-Control":"max-age=0",
	"User-Agent":"Mozilla/5.0 (Windows NT 10.0;WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
	"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
	"Accept-Encoding":"gzip,deflate,sdch,br",
	"Accept-Language":"zh-CN,zh;q=0.8"
	}

proxies = {'http':"http://121.232.147.28:9000"}

#download search page
def search_pages(keywords):
	try:
		response = requests.get('https://aso100.com/search?country=cn&search={0}'.
			format(keywords),headers=headers,proxies=proxies)
		if response.status_code != 200:
			print("-> {0}: Page error........{1}".format(keywords,response.status_code))
	except requests.URLRequired:
		print(" -> A valid URL is required to make a reques.\n")
	except requests.ConnectionError:
		print(" -> Network connection error.\n")
		sys.exit()
	except requests.HTTPError:
		print(" -> An HTTP error occurred.\n")
	except (requests.Timeout,requests.ConnectTimeout) as e:
		print(" -> The request or trying to connect servertimed out.\n")
	else:
		time.sleep(random.randint(1,5))
	return response.content

#获取Appstore排名List
def get_appstore_ranking_results(page):
	expected_title = u'搜索结果'
	appstore_results = []
	soup = BeautifulSoup(page,'html.parser')
	# soup.prettify() 指定编码,格式化输出
	try:
		soup_title= soup.title.prettify()
		response_title = soup_title.replace("<title>","").replace("</title>","").strip()
		if expected_title in response_title:
			print("\n {0}..........................ok \n".format(response_title.encode("gbk")))
		else:
			print(response_title)
			sys.exit()
		try:
			appstore_results = [ranking for applist in soup.find_all(class_="app-list") 
						for rankList in applist.find_all('h4',class_="media-heading") 
						for ranking in rankList.find('a')]
		except Exception,e:
			print(e)
		else:
			print(json.dumps(appstore_results, encoding="UTF-8", ensure_ascii=False))
	except Exception,e:
		pass
	return appstore_results

#关键词搜索,前20名搜索结果
# result = []
# for keyword in ios_app_keywords:
# 	result.append(get_appstore_ranking_results(search_pages(keyword)))
# print(json.dumps(dict(zip(ios_app_keywords,result)), encoding="UTF-8", ensure_ascii=False))

#筛选出包括特定包名的搜索结果
keyword_ranking = [r for keyword in ios_app_keywords for r in get_appstore_ranking_results(search_pages(keyword)) if appName in r ]
print json.dumps(dict(zip(ios_app_keywords,keyword_ranking)), encoding="UTF-8", ensure_ascii=False)