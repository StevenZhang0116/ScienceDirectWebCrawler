#!/usr/bin/python
#coding=UTF-8

import traceback
import numpy as np

from .crawler_db import *

__all__=['KeywordPdfSummary']

class KeywordPdfSummary:
	'''
	'''

	def __init__(self):
		'''
		'''
		self.data=None

	def run(self):
		'''
		'''
		ret=self.build_data()
		if ret:
			ret=self.build_report()

		return ret

	def build_report(self):
		'''
		'''
		df=self.data
		rpt={}

		ret=True

		for index,rec in df.iterrows():
			taskid=rec['t_taskid']
			item=rpt.get(taskid)
			if item is None:
				item={
					'taskid':taskid,
					'0':0,
					'1':0,
					'total':0,
					'done':0
				}
				rpt[taskid]=item

			state=rec['t_state']
			cnt=rec['cnt']
			item[f'{state}']=cnt

		w0=12;w1=12;w2=12;w3=12;w4=8

		print(f'{"taskid":<{w0}}',end=' ')
		print(f'{"unfinished":>{w1}}',end=' ')
		print(f'{"finished":>{w2}}',end=' ')
		print(f'{"total":>{w3}}',end=' ')
		print(f'{"done%":>{w4}}')

		print('-'*w0,end=' ')
		print('-'*w1,end=' ')
		print('-'*w2,end=' ')
		print('-'*w3,end=' ')
		print('-'*w4)

		for key,item in rpt.items():
			
			item['total']=item['0']+item['1']
			item['done']=np.round(item['1']*100/item['total'],2)

			print(f'{item["taskid"]:<{w0}}',end=' ')
			print(f'{item["0"]:>{w1}}',end=' ')
			print(f'{item["1"]:>{w2}}',end=' ')
			print(f'{item["total"]:>{w3}}',end=' ')
			print(f'{item["done"]:>{w4}}')

		return ret


	def build_data(self):
		'''
		'''
		ret=True

		sql='''
			select t_taskid,t_state,count(*) as cnt from dl_pdf_tasks
			group by t_taskid,t_state
			order by t_taskid
		'''

		db=CrawlerDB()
		dh=db.getHandle()

		try:
			dh.open()
			self.data=dh.executeQuery(sql)
			dh.close()
			ret=True
		except Exception as ex:
			dh.close()
			ret=False
			traceback.print_exc()

		return ret



