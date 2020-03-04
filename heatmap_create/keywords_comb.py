import pandas as pd
import math
import numpy as np
#import urllib2
# This code is purposed to generate keyword combinations based the given csv file

#------------------
#
#------------------
class searchUrlBuilder:
	#---------------
	#
	#---------------
	def __init__(self):
		self.target_url='https://www.sciencedirect.com/search/advanced?qs=%20'
		# self.default_keyfile='/Users/stevenzhang/Desktop/keywords.csv'
		self.default_keyfile='./keywords.csv'
		
		self.url_list=[]
		self.url_caller=None

	#---------------
	#
	#---------------
	def build(self,filepath=None,url_caller=None):

		self.url_caller=url_caller

		if (filepath is None) or (len(filepath)<=0):
			filepath=self.default_keyfile
		
		df=pd.read_csv(filepath)

		cols=[]
		# cols=['keyword1','keyword2']
		for col in df.columns:
			if col.startswith('keyword'):
				cols.append(col)

		if len(cols)<=0:
			print(f'[error]:no keyword columns in key-file.')
			return None

		cidx=0

		self.url_list.clear()
		self.build_url([],df,cols,cidx)
		return self.url_list

	#-------------
	#
	#-------------
	def build_url(self,cas,df,cols,idx):

		cname=cols[idx]
		col=df[cname].copy()
		col.dropna(inplace=True)
		cvals=col.tolist()
		# print(cvals)

		nidx=idx+1

		for cval in cvals:
			ncas=cas.copy()
			ncas.append(cval)
			if nidx<len(cols):
				self.build_url(ncas,df,cols,nidx)
			else:
				self.create_url(ncas)

	#---------------
	#
	#---------------
	def create_url(self,items):
		# print(f'items:({items})')
		its=[]
		for item in items:
			nit=self.encode_url_item(item)
			its.append(nit)

		sval='%20AND%20'.join(its)
		sval=f'{self.target_url}{sval}'

		if self.url_caller is not None:
			self.url_caller(sval)
		else:
			self.url_list.append(sval)

	#----------------
	#
	#----------------
	def encode_url_item(self,item):
		ais=item.split()
		sval='%20'.join(ais)
		sval=f'"{sval}"'
		return sval

#--------
# Testing
#--------

def ucaller(url):
	print(f'[ucaller]:({url})')

builder=searchUrlBuilder()
lst=builder.build(url_caller=ucaller)

lst=builder.build()

with open("/Users/stevenzhang/Desktop/sciencedirect/keywords_combination_list.csv", "wt") as f:
	for i in lst:
		print(i, file = f)

























