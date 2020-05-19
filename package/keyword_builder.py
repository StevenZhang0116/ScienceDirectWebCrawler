#!/usr/bin/python
#coding=UTF-8

import traceback
from .search_url_builder import *
from .crawler_db import *
from .date_time import *


__all__=['KeywordBuilder']

class KeywordBuilder:
	'''
	'''
	def __init__(self,task_id,file_path):
		'''
		'''
		self.task_id=task_id
		self.file_path=file_path
		self.build_cnt=0

	@property
	def buildCount(self):
		return self.build_cnt

	def run(self):
		'''
		'''
		task_id=self.task_id
		fpath=self.file_path

		self.build_cnt=0

		sub=SearchUrlBuilder()

		db=CrawlerDB()
		dh=db.getHandle()

		um=UniqueIdMaker()
		today=DateTime.today()
		dts=today.toDateString()

		def url_maker(url,keys):
			t_recid=um.create()

			rec={
				't_recid':t_recid,
				't_taskid':task_id,
				'kw1':keys[0],
				'kw2':keys[1],
				'crdt':dts,
				'mddt':dts
			}

			dh.insert('dl_keys',rec)

			rec={
				't_recid':t_recid,
				't_keyid':t_recid,
				't_taskid':task_id,
				't_url':url,
				'crdt':dts,
				'mddt':dts		
			}

			dh.insert('dl_tasks',rec)
			self.build_cnt+=1

		ret=True
		try:
			dh.open()
			dh.begin()

			sub.build(fpath,url_maker)

			dh.commit()
			dh.close()

			ret=True
		except Exception as ex:
			self.build_cnt=0
			dh.rollback()
			dh.close()
			ret=False
			traceback.print_exc()

		return ret




