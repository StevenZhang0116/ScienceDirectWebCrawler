#!/usr/bin/python
#coding=UTF-8

from bs4 import BeautifulSoup
import urllib.request

import ssl

import traceback
import re
import json
import threading

from .web_page import *
from .cr_logger import *

__all__=['SearchResultPage']

class SearchResultPage(WebPage):
	'''
	'''
	def __init__(self,search_url):
		'''
		'''

		super().__init__()

		self.search_url=search_url
		self.soup=None
		self.result_count=0
		self.keyword1=None
		self.keyword2=None

		self.num_of_page=100
		self.all_url_coll=[]
		self.pdf_urls=[]

		self.logger=Logger('SearchPage')

	def getPdfUrls(self):
		'''
		'''
		return self.pdf_urls

	def process(self):
		'''
		'''
		ret=False

		self.logger.info(f'[process]:url({self.search_url})')

		try:
			ret=self.process_req()
		except Exception as ex:
			traceback.print_exc()
			ret=False

		self.logger.info(f'[process]:done.ret({ret})')

		return ret

	def process_req(self):
		'''
		'''
		ret=self.request_data()
		if ret:
			ret=self.parse_keyword_info()

		if ret:
			ret=self.build_all_urls()

		if ret:
			ret=self.find_pdf_urls()

		return ret


	def find_pdf_urls(self):
		'''
		clone from find_name_url(sample,path) in main.py
		'''
		all_url_coll = self.all_url_coll

		ret=True

		pdf_urls=[]

		for url in all_url_coll:

			url = url.replace("\n", "")
			
			self.logger.info(f'[parse-url]:({url})')

			soup=self.get_soup(url)
			js_items=self.find_js_data(soup)

			for item in js_items:
				rit=self.create_result_item(item)
				pdf_urls.append(rit)

		self.pdf_urls=pdf_urls

		return ret

	def create_result_item(self,item):
		'''
		'''
		ret={}
		names=[
			'contentType','documentSubType','doi',
			'publicationDate','sourceTitle','title',
			'articleType','issn','isbn'
			]

		for name in names:
			val=item.get(name,'')
			ret[name]=val

		sub=item.get('pdf')
		if sub is not None:
			val=sub.get('downloadLink','')
			ret['url']=val
		else:
			ret['url']=''

		ret['name']=item['title']

		sub=item.get('authors')
		if sub is not None:
			ret['authors']=sub

		return ret

	def find_js_data(self,soup):
		'''
		'''
		
		ret=[]
		body=soup

		pattern=re.compile(r'var INITIAL_STATE = (.*?)',re.MULTILINE|re.DOTALL)
		script=body.find('script',text=pattern)

		data=''
		if script is not None:
			data=script.text
			data=data.replace('var INITIAL_STATE = ','')
			data=data.replace(':undefined',':""')
			# data=data.replace(':null',':""')

		# print(f'script:({data})')
		if data=='':
			self.logger.error(f'[FATAL]:not found script-data.')
			# with open(path + '/script_data.htm','w') as fp:
			# 	fp.write(f'{body}')
		else:

			# with open(path + '/script_data.htm','w') as fp:
			# 	fp.write(f'{body}')

			# with open(path + '/script_data.json','w') as fp:
			# 	fp.write(data)

			jobj=json.loads(data)
			# print(f'script:load ok.')
			srs=jobj['search']['searchResults']
			# print(f'srs:({srs})')
			ret=srs

			# sval=json.dumps(jobj,indent=3)
			# with open(path + '/script_data-well-format.json','w') as fp:
			# 	fp.write(sval)

		return ret		

	def build_all_urls(self):
		'''
		clone from all_url_find(basic_url,num_of_page=100) in find_pdf.py
		'''

		ret=True
		basic_url=self.search_url
		num_of_page=self.num_of_page

		all_url_coll = []
		count = self.result_count

		self.logger.info(f"[build_all_urls]:result_count:({count})")
		remainder = int(count) // num_of_page
		for i in range(remainder+1):
			new_url=f'{basic_url}&show={num_of_page}&offset={str(i*num_of_page)}'
			all_url_coll.append(new_url)

		self.all_url_coll=all_url_coll
		return ret


	def parse_keyword_info(self):
		'''
		clone from result_keyword_find method in find_count.py
		'''

		ret=True

		sval = self.soup.title.text
		sval = sval.strip()

		self.logger.info(f'[parse_keyword_info]:title({sval})')

		pos = sval.find(" ")
		count = sval[0:pos]
		count=count.replace(',','')

		cut = []
		for i in range(len(sval)):
			if sval[i] == "\"":
				cut.append(i)

		keyword1 = sval[cut[0]+1:cut[1]]
		keyword2 = sval[cut[2]+1:cut[3]]

		self.result_count=count
		self.keyword1=keyword1
		self.keyword2=keyword2

		return ret

	def request_data(self):
		'''
		clone from test_title method in htm_saver.py
		'''
		ret=False
		url=self.search_url
		soup=self.get_soup(url)
		if soup is not None:
			self.soup=soup
			ret=True

		return ret

	def get_soup(self,url):
		'''
		clone from get_soup method in htm_saver.py
		'''

		ssl._create_default_https_context = ssl._create_unverified_context

		req=urllib.request.Request(url)
		uagent=self.userAgent

		req.add_header('User-Agent',uagent)

		ret=True
		page=None

		try:
			page=urllib.request.urlopen(req)
		except Exception as ex:
			traceback.print_exc()
			page=None
			ret=False

		soup=None
		if ret:
			try:
				soup=BeautifulSoup(page,'html.parser')
			except Exception as ex:
				traceback.print_exc()
				soup=None
				ret=False

		return soup


