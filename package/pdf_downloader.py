#!/usr/bin/python
#coding=UTF-8

import os
import requests

from bs4 import BeautifulSoup

import urllib.request

import urllib.parse as urlp
import csv
import ssl

import random
import traceback
import re
import json

from .cr_logger import *

__all__=['PdfDownloader']

#-----------
#
#-----------
class PdfDownloader:
	'''
	'''
	def __init__(self,session_id,save_folder=None,do_debug=False):
		self.pdf_url=None
		self.pdf_file_name=None
		self.save_folder=save_folder
		self.user_agent=self.select_user_agent()

		self.save_remote=False
		self.session_id=session_id

		self.content_data=None

		self.logger=Logger('Downloader')


	def getContentData(self):
		'''
		'''
		ret=self.content_data
		return ret

	#-------
	#
	#-------
	def download(self,url):
		'''
		'''
		ret=self.parse_request_url(url)
		
		if ret:
			ret=self.check_save_folder()

		if ret:
			ret=self.request_pdf_url(url)

		if ret:
			ret=self.download_pdf(self.pdf_url)

		return ret

	def check_save_folder(self):
		'''
		'''
		ret=True

		if self.save_folder is None:
			# self.save_folder='./pdf_files'
			return ret

		fpath=self.save_folder

		if not os.path.exists(fpath):
			try:
				os.makedirs(fpath)
			except Exception as ex:
				ret=False
				self.logger.error(f'[check_save_folder][exception]:folder({fpath})')
				self.logger.error(f'[check_save_folder][exception]:ex({ex})')
				traceback.print_exc()

		return ret

	#-------
	#
	#-------
	def parse_request_url(self,url):
		'''
		'''
		ret=True
		items=None
		try:
			up=urlp.urlparse(url)
			qsl=urlp.parse_qsl(up.query)
			items=dict(qsl)
		except Exception as ex:
			self.logger.error(f'[parse_request_url][exception]:url({url})')
			self.logger.error(f'[parse_request_url][exception]:ex({ex})')
			traceback.print_exc()
			ret=False
			items=None

		if ret:
			pid=items.get('pid')
			if pid is None:
				self.logger.error(f'[parse_request_url][error]:no (pid) in url.')
				ret=False
			else:
				self.pdf_file_name=pid

		return ret


	#--------
	#
	#--------
	def select_user_agent(self):
		'''
		'''
		optional_headers=[
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

		uagent=random.choice(optional_headers)
		return uagent

	#---
	#
	#---
	def save_soup(self,soup):
		'''
		'''
		ret=True
		fpath='./find_pdf.htm'

		self.logger.warn(f'[save_soup]:fpath({fpath})')
		try:
			with open(fpath,'w') as fp:
				fp.write(f'{soup}')
			ret=True
		except Exception as ex:
			self.logger.error(f'[save_soup][exception]:ex({ex})')
			ret=False

		self.logger.warn(f'[save_soup]:done.ret({ret})')

	#---------
	#
	#---------
	def request_pdf_url(self,url):
		'''
		'''
		self.logger.debug(f'[request_pdf_url]:url({url})')

		self.pdf_url=None

		# headers={
		# 	'User-Agent':self.user_agent
		# }

		headers={
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
			'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'
		}

		cookies=None
		if (self.session_id is not None) and (self.session_id!=""):
			cookies={}
			cookies['sd_session_id']=self.session_id


		ret=True
		req=None

		timeout=(30,30)

		try:
			req=requests.get(url,headers=headers,cookies=cookies,timeout=timeout)
		except Exception as ex:
			self.logger.error(f'[request_pdf_url][exception]:url({url}) ex({ex})')
			traceback.print_exc()
			ret=False

		if self.save_remote:
			with open("requests.htm",'wb') as f:
			    f.write(req.content)

		soup=None

		if ret:
			self.logger.debug(f'[request_pdf_url]:req-type:({type(req)})')
			try:
				soup=BeautifulSoup(req.content,'html.parser')					
			except Exception as ex:
				self.logger.error(f'[request_pdf_url][exception]:({ex})')
				traceback.print_exc()
				soup=None
				ret=False

		if ret:

			self.logger.debug(f'[request_pdf_url]:soup-type:({type(soup)})')

			pattern=re.compile(r'window.location = (.*?)',re.MULTILINE|re.DOTALL)
			script=soup.find('script',text=pattern)
			if script is None:
				self.logger.error(f'[request_pdf_url][error]:no found (window.location)')
				ret=False
			else:
				data=script.text
				rets=re.findall(r"window.location = '(.*?)'",data)
				if rets is not None:
					self.pdf_url=rets[0]
				else:
					self.logger.error(f'[request_pdf_url][error]:parse location FAILED.')
					ret=False

			if ret==False:
				self.logger.error([
					f'[request_pdf_url][error]:maybe wrong session_id.',
					f'session_id=({self.session_id})',
					f'session_id set in app_config.py'
					])
				self.save_soup(soup)

		return ret

	#-------
	#
	#-------
	def download_pdf(self,url):
		'''
		'''
		self.logger.debug(f'[download_pdf]:url({url}).')

		headers={
			'User-Agent':self.user_agent
		}

		ret=True
		req=None

		try:
			req=requests.get(url,headers=headers)
			self.content_data=req.content

		except Exception as ex:
			self.logger.error(f'[download_pdf][exception]:url({url})')
			self.logger.error(f'[download_pdf][exception]:ex({ex})')
			traceback.print_exc()
			ret=False

		if ret and (self.save_folder is not None):
			save_file=f'{self.save_folder}/{self.pdf_file_name}'
			self.self.logger.debug(f'[download_pdf]:save to ({save_file})')
			try:
				with open(save_file,'wb') as f:
					f.write(req.content)
			except Exception as ex:
				self.logger.error(f'[download_pdf][exception]:save_file({save_file})')
				self.logger.error(f'[download_pdf][exception]:({ex})')
				traceback.print_exc()
				ret=False

		self.logger.debug(f'[download_pdf]:done.ret({ret})')

		return ret

#----------
# for test
#----------
if __name__=='__main__':

	#-----
	# for testing.
	#-----
	image_url="http://www.sciencedirect.com/science/article/pii/S2211425412000192/pdfft?md5=d0c9cd7d4c7d439d508e0d433fc04184&pid=1-s2.0-S2211425412000192-main.pdf"

	# we need parse web-page to get real pdf url as following:
	# pdf_url="https://pdf.sciencedirectassets.com/280663/1-s2.0-S2211425412X00037/1-s2.0-S2211425412000192/main.pdf?X-Amz-Security-Token=IQoJb3JpZ2luX2VjEA4aCXVzLWVhc3QtMSJGMEQCIGFrFTOjJ4RO5bk8%2FgVlQzGlaKevJL7nFMV5hVG8YQt%2BAiAZmDKaVG9mf21Qy%2FAFePuvj0nu9yDCvjgrtlJEGi%2BGMSq9AwjW%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F8BEAIaDDA1OTAwMzU0Njg2NSIMSFtS6GIw8zdEVIe%2BKpEDa7op%2FnUaYmY753D25anW008iUSRHioawU8TSPImUG%2BgYdB5K%2B85ockLJ6N2kJBA7VFobkrtbrZA2G4WcY2B5NazIbc9Bg7xKIKrIEk1pUdpa4P2MDfulIG3ST4eSZ9G0PiAPByd%2B6sY49TB4ePTJkAT7ZgJGjftbVIS1ioPVeCH5Ccx%2F%2Bz6nn%2B93WqCOh671CRlyf2IqMdmf48XXaXykrUoEyTOi0rbFQveWk1z3xJzcpfb5%2FfqoVxTsuZuBnczlxmVuGQWZ7dw2VYp6cfs4MQVGTjxwphvgxDBl05kGyzQYucc7EmMEqtyhUgvh9lYP6y1l9Wo43vzuQlIkUKxDVFM43rPBfa66sQRTPe%2FI86Jjo2kb5zySikpL%2FeHvEJ%2BHLRopWop2UfMpI9DIjS1KDyIJi9fpGSl0FE4qf0vcimwUT5Go2rsaonmcNF7SoLnitEMMLsiphsACp%2FBZvfef8eCFjFydGMxc%2FNYHTDKbUiJsjgaZINaWc8blp%2BhwVsBnqwjcXkarWMQDiZiMUVwNrOAw46bk8gU67AHHtuy8J2D6bjFTA9J%2B9fYbaba6GAfd%2BSaAMBBpAh3YwILgfEni7kBDVFuorpTXtB%2BfXQoUxKVbGtQyBHYUW5jtn5XqW77K4bIrSlbflIO%2FdTSUESb0jeqyf5Ro7aVaT2Oslp921I0r58dInxefMqkMdsntDqosMS5eOQqnzLgMGKXZ5Gpq2MSFgu%2Fg7WgOp%2BhtjhyiS9pRw9g8a9Mv8Jy9pCRzc9HXMlYlELBmXLBl4e0b9Wi8xsuHtr%2BiE7K0JC849H5Mh%2B9fdijOyB%2FbqV1KEy%2B7LsqXnzINLJKGcv685eYw1TdTM64bcyOYDg%3D%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20200228T135910Z&X-Amz-SignedHeaders=host&X-Amz-Expires=300&X-Amz-Credential=ASIAQ3PHCVTY4XEUXAAM%2F20200228%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=86234d12de9e3207a2b2b909ac3eb7f0038aa237ede69e80e51c3af525f535b1&hash=92f66ae454ebce74ce415a9981d0ff3bfdce1f82d3742bc2710afab648bccf5e&host=68042c943591013ac2b2430a89b270f6af2c76d8dfd086a07176afe7c76c2c61&pii=S2211425412000192&tid=spdf-b7c98c28-e79a-49ec-a6ca-b908a8580593&sid=6894d4f04781474e951b4ef39b3d9c91f792gxrqa&type=client"

	print(f'[main].')
	dl=PdfDownloader()
	ret=dl.download(image_url)
	print(f'[main]:done.ret({ret})')





