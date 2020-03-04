#!/usr/bin/python
#coding=UTF-8

from bs4 import BeautifulSoup
import urllib.request
import csv
import ssl


import random
import traceback
import re
import json

import re

# This part of code is purposed to save read the TITLE part of the htm from the webpage
# get access to the information directly without saving the htm file to save space and improve efficiency. 

my_headers = [
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
    'Opera/9.25 (Windows NT 5.1; U; en)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
    'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
    "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
    "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 "
]


def test_result(g_targetURL):
	result = None

	# print(f'[test_1].')
	url=g_targetURL	
	ssl._create_default_https_context = ssl._create_unverified_context

	req=urllib.request.Request(url)
	uagent=random.choice(my_headers)

	# print(f'[test_1]:url({url})')
	# print(f'[test_1]:user-agent({uagent})')

	req.add_header('User-Agent',uagent)

	ret=True
	page=None

	try:
		page=urllib.request.urlopen(req)
		# print(f'page({type(page)})')
	except Exception as ex:
		# print(f'[test_1][exception]:({ex})')
		traceback.print_exc()
		page=None
		ret=False

	soup=None
	if ret:
		try:
			soup=BeautifulSoup(page,'html.parser')
			# print(f'soup({type(soup)})')
			# print(soup)
			parse_soup(soup)
		except Exception as ex:
			# print(f'[test_1][exception]:({ex})')
			traceback.print_exc()
			soup=None
			ret=False

	result = parse_soup(soup)
	return result



	# if ret:
	# 	try:
	# 		fp=open('./soup.htm','w')
	# 		fp.write(f'{soup}')
	# 		fp.close()
	# 	except Exception as ex:
	# 		print(f'[test_1][exception]:({ex})')
	# 		traceback.print_exc()
	# 		print(f'save soup Failed.')

	# print(f'[test_1]:done.ret({ret})')


def parse_soup(soup):
	ret = None
	ret = search_result(soup)
	return ret

def search_result(soup):
	title = soup.title
	return title

	#print(target)

# def find_script_var(soup):
# 	pattern=re.compile(r'var INITIAL_STATE = (.*?)',re.MULTILINE|re.DOTALL)
# 	script=soup.find('script',text=pattern)
# 	if script is None:
# 		print(f'[find_script_var][warning]:not found INITIAL_STATE.')
# 		return

# 	data=script.text
# 	pos=data.find('=')
# 	print(f'[find_script_var]:find pos=({pos})')
# 	if pos>0:
# 		data=data[pos+1:]
# 		data=data.strip()

# 	print(f'[find_script_var]:save to json file.')
# 	try:
# 		fp=open('./INITIAL_STATE.json','w')
# 		fp.write(f'{data}')
# 		fp.close()
# 	except Exception as ex:
# 		print(f'[find_script_var][exception]:({ex})')
# 		traceback.print_exc()

# 	print(f'[find_script_var]:save done.')


def main_routine():
	test_result()


